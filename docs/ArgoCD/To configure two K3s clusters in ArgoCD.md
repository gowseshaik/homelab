To configure **two K3s clusters in ArgoCD**, follow these **first-principle steps**:

### 🔧 Prerequisites (on the machine where ArgoCD CLI is installed):

1. You must have `argocd` CLI.
2. You must have access to both clusters via `~/.kube/config`.
3. You must be logged into ArgoCD:

```bash
argocd login <ARGOCD_SERVER> --username admin --password <PASSWORD> --insecure
$ argocd login argocd.local --username admin --password admin123 --insecure
# Note: you should login without "http://"

```

### 🪛 Step-by-step Commands:

#### 1️⃣ Add first cluster to ArgoCD

```bash
gouse@gouse:~/DevOps/multipass_scripts$ kubectl config get-contexts
CURRENT   NAME          CLUSTER       AUTHINFO   NAMESPACE
*         dev-context   devcluster    dev-user   
          prd-context   prd-cluster   prd-user   

argocd cluster add dev-context --name devcluster --insecure

argocd cluster add k3s-user@k3s-cluster --name dev-cluster


gouse@gouse:~/DevOps/multipass_scripts$ argocd cluster add dev-context --name devcluster --insecure
WARNING: This will create a service account `argocd-manager` on the cluster referenced by context `dev-context` with full cluster level privileges. Do you want to continue [y/N]? y
{"level":"info","msg":"ServiceAccount \"argocd-manager\" created in namespace \"kube-system\"","time":"2025-07-03T14:00:15+03:00"}
{"level":"info","msg":"ClusterRole \"argocd-manager-role\" created","time":"2025-07-03T14:00:15+03:00"}
{"level":"info","msg":"ClusterRoleBinding \"argocd-manager-role-binding\" created","time":"2025-07-03T14:00:15+03:00"}
{"level":"info","msg":"Created bearer token secret for ServiceAccount \"argocd-manager\"","time":"2025-07-03T14:00:15+03:00"}
{"level":"warning","msg":"Failed to invoke grpc call. Use flag --grpc-web in grpc calls. To avoid this warning message, use flag --grpc-web.","time":"2025-07-03T14:00:16+03:00"}
Cluster 'https://10.189.65.115:6443' added
```

> `k3s-user@k3s-cluster` matches the context name in your `~/.kube/config`

#### 2️⃣ Add second cluster to ArgoCD

```bash
argocd cluster add k3s-user@k3s-prod-cluster --name prod-cluster


argocd cluster add prd-context --name prd-cluster --insecure
gouse@gouse:~/DevOps/multipass_scripts$ argocd cluster add prd-context --name prd-cluster --insecure
WARNING: This will create a service account `argocd-manager` on the cluster referenced by context `prd-context` with full cluster level privileges. Do you want to continue [y/N]? y
{"level":"info","msg":"ServiceAccount \"argocd-manager\" created in namespace \"kube-system\"","time":"2025-07-03T14:01:47+03:00"}
{"level":"info","msg":"ClusterRole \"argocd-manager-role\" created","time":"2025-07-03T14:01:47+03:00"}
{"level":"info","msg":"ClusterRoleBinding \"argocd-manager-role-binding\" created","time":"2025-07-03T14:01:47+03:00"}
{"level":"info","msg":"Created bearer token secret for ServiceAccount \"argocd-manager\"","time":"2025-07-03T14:01:47+03:00"}
{"level":"warning","msg":"Failed to invoke grpc call. Use flag --grpc-web in grpc calls. To avoid this warning message, use flag --grpc-web.","time":"2025-07-03T14:01:48+03:00"}
Cluster 'https://10.189.65.110:6443' added
```

> Make sure your kubeconfig has a second context for the prod cluster, like:

```yaml
- name: k3s-prod-cluster
  context:
    cluster: k3s-prod
    user: k3s-user
```

### ✅ Validate

Check both clusters registered:

```bash
argocd cluster list
argocd cluster list --grpc-web

# 1. Check ArgoCD server URL you are talking to
argocd context

# 2. Add cluster explicitly with kubeconfig path and grpc-web flag
argocd cluster add https://10.189.65.115:6443 --grpc-web

# 3. Verify cluster is added
argocd cluster list --grpc-web

gouse@gouse:~/DevOps/multipass_scripts$ argocd cluster list --grpc-web
SERVER                          NAME         VERSION  STATUS   MESSAGE                                                  PROJECT
https://10.189.65.110:6443      prd-cluster           Unknown  Cluster has no applications and is not being monitored.  
https://10.189.65.115:6443      devcluster            Unknown  Cluster has no applications and is not being monitored.  
https://kubernetes.default.svc  in-cluster            Unknown  Cluster has no applications and is not being monitored.  


# 4. Try to create app again
argocd app create guestbook \
  --repo https://github.com/argoproj/argocd-example-apps.git \
  --path guestbook \
  --dest-server https://10.189.65.115:6443 \
  --dest-namespace default \
  --sync-policy automated \
  --grpc-web

argocd app create guestbook-prd \
  --repo https://github.com/argoproj/argocd-example-apps.git \
  --path guestbook \
  --dest-server https://10.189.65.110:6443 \
  --dest-namespace default \
  --sync-policy automated \
  --grpc-web

```

### 📝 Sample `~/.kube/config` should have 2 contexts:

```yaml
contexts:
- name: k3s-cluster
  context:
    cluster: k3s-cluster
    user: k3s-user
- name: k3s-prod-cluster
  context:
    cluster: k3s-prod
    user: k3s-user
```

### 💡 Why it's needed --grpc:
We use `--grpc-web` with the `argocd` CLI when **the ArgoCD API server is exposed through a reverse proxy (like NGINX, Ingress, etc.) that only supports HTTP/1.1** — and not native gRPC (which needs HTTP/2).

ArgoCD CLI by default uses **gRPC over HTTP/2**, but many Ingress controllers or proxies:
- **don’t support raw gRPC**, or
- **strip HTTP/2 headers**, breaking gRPC calls.

To bypass this, `--grpc-web` makes the CLI use **gRPC-Web** (gRPC over HTTP/1.1 + JSON encoding), which is more compatible with typical reverse proxies and ingress setups.

### ✅ When to use:

Use `--grpc-web` **if:**

- You access ArgoCD behind an ingress controller (e.g. NGINX Ingress).
- You get errors like:
    - `Failed to invoke grpc call`
    - `rpc error: code = Unavailable desc = transport is closing`
    - `connect: connection refused` for gRPC
### ❌ When not needed:

- If ArgoCD is directly exposed on a LoadBalancer IP or NodePort **without any ingress or proxy**, and supports **HTTP/2**, then `--grpc-web` is **not required**.
### Tip:

You can set it as default to avoid adding every time:
```bash
alias argocd='argocd --grpc-web'
```
Or set context-wide config (manually) via env or wrapper.
