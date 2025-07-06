<span style="color:#4caf50;"><b>Created:</b> 2025-07-06</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

### 🔁 **How ArgoCD and OpenShift Work Together**

|**Tool**|**Purpose**|**Typical Use in DevOps**|
|---|---|---|
|**ArgoCD**|GitOps continuous delivery for Kubernetes|Sync Kubernetes manifests from Git repos automatically|
|**OpenShift**|Enterprise Kubernetes platform with enhanced security & UI|Hosts clusters, manages RBAC, provides developer-friendly UI|
### 🔧 **Common Use Case**

> **ArgoCD manages app deployments** into an **OpenShift (OCP) cluster**, syncing Git-based manifests or Helm charts. OpenShift provides the platform, ArgoCD handles the delivery.

### 🧨 **DevOps Challenges (When Using ArgoCD on OpenShift)**

|**Problem Area**|**Details**|**Impact**|
|---|---|---|
|**RBAC Conflict**|OpenShift's stricter SecurityContextConstraints (SCC) may block ArgoCD apps unless configured|Pods won't start or get permission denied|
|**ServiceAccount Confusion**|ArgoCD needs its own ServiceAccount with correct roles; often users forget to bind `edit` or `admin` on target namespaces|ArgoCD syncs fail with `permission denied`|
|**Ingress Differences**|OpenShift routes vs Kubernetes Ingress objects behave differently|ArgoCD apps fail unless OpenShift Route is created properly|
|**ImagePull Secrets**|OpenShift requires secrets to be attached in a specific way|ArgoCD deployments pull image errors|
|**Resource Quota Limits**|OCP enforces limits (CPU/Memory/Pod count) tightly|ArgoCD sync gets stuck or partially applied apps|
|**Sync Failures**|SCCs or OCP admission controllers reject certain deployments (e.g., privileged containers, hostPaths, etc.)|ArgoCD shows `Health: Degraded`|
|**TLS & Route Conflicts**|OpenShift automatically handles routes; deploying ingress.yaml via ArgoCD can conflict|ArgoCD-managed ingress won’t reflect correctly in OCP UI|
|**ArgoCD Console Access**|In OpenShift Console, ArgoCD UI is external unless set up with OAuth proxy or Route|Requires manual `oc expose svc/argocd-server` or Route CR|
### ✅ **Best Practices**

|**Category**|**Best Practice**|
|---|---|
|RBAC|Bind `argocd` SA to `edit` or higher role on target namespaces|
|SCC|Use custom SCCs with `runAsNonRoot` if needed; avoid default `restricted` profile for ArgoCD apps|
|Route Management|Let OpenShift handle Routes; avoid managing Ingress via ArgoCD unless explicitly supported|
|Image Management|Use OpenShift internal registry or ensure imagePullSecrets are in the same namespace|
|ArgoCD Namespace Control|Use ArgoCD Projects to limit access to namespaces, resources, and source repos|
|OAuth Integration|Use `argocd-dex` with OpenShift OAuth provider for smoother login|
|Resource Limits|Ensure ArgoCD apps specify resource requests/limits to comply with OpenShift quotas|
### 🔗 **Typical Real-World Command Flow**

```sh
# Install ArgoCD in OpenShift (namespace: argocd)
oc new-project argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Expose ArgoCD UI on OpenShift
oc expose svc/argocd-server -n argocd --port=http

# Login to ArgoCD CLI
argocd login <argo_route_url> --username admin --password <initial_password> --grpc-web

# Create app that deploys to OpenShift project 'dev'
argocd app create my-app \
  --repo https://github.com/example/repo.git \
  --path manifests \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace dev \
  --sync-policy automated

# Give ArgoCD service account access to 'dev' project
oc adm policy add-role-to-user edit system:serviceaccount:argocd:argocd-application-controller -n dev
```
