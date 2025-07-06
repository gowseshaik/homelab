<span style="color:#4caf50;"><b>Created:</b> 2025-07-01</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

# ingress access 
```
# argocd-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: argocd-ingress
  namespace: argocd
spec:
  ingressClassName: traefik
  rules:
    - host: argocd.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: argocd-server
                port:
                  number: 80
```

```
k get ingress -n argocd
```

update /etc/hosts file
```
sudo sh -c "echo '<multipass-any-node-ip> argocd.local' >> /etc/hosts"
```

deployment patch for `--insecure` access for argocd url http://argocd.local
```
kubectl -n argocd patch deployment argocd-server \
  --type='json' \
  -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/args", "value": ["/usr/local/bin/argocd-server", "--insecure"]}]'
```

### get admin password
```bash
$ kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo

$ FNLoqZlqBZry3Gcc
```

### ✅ Install Argo CD CLI (Linux)

```bash
VERSION=$(curl -s https://api.github.com/repos/argoproj/argo-cd/releases/latest | grep tag_name | cut -d '"' -f 4)

curl -sSL -o argocd "https://github.com/argoproj/argo-cd/releases/download/${VERSION}/argocd-linux-amd64"

chmod +x argocd
sudo mv argocd /usr/local/bin/
```

### 🔍 Verify

```bash
argocd version
```

Should output CLI and server versions (CLI only if not logged in yet).

### ✅ Login to Argo CD

```bash
$ argocd login argocd.local --username admin --password <current-password> --insecure

$ argocd login argocd.local --username admin --password FNLoqZlqBZry3Gcc --insecure


gouse@gouse:~/DevOps/multipass_scripts$ argocd login argocd.local --username admin --password FNLoqZlqBZry3Gcc --insecure
{"level":"warning","msg":"Failed to invoke grpc call. Use flag --grpc-web in grpc calls. To avoid this warning message, use flag --grpc-web.","time":"2025-06-30T22:28:33+03:00"}
'admin:login' logged in successfully
Context 'argocd.local' updated
```

> `--insecure` is required if you're using plain HTTP or self-signed TLS.

---

### 🔐 Change Password

```bash
argocd account update-password --current-password <current-password> --new-password <new-password>

argocd account update-password --current-password FNLoqZlqBZry3Gcc --new-password admin123

gouse@gouse:~/DevOps/multipass_scripts$ argocd account update-password --current-password FNLoqZlqBZry3Gcc --new-password admin123
{"level":"warning","msg":"Failed to invoke grpc call. Use flag --grpc-web in grpc calls. To avoid this warning message, use flag --grpc-web.","time":"2025-06-30T22:29:33+03:00"}
Password updated
Context 'argocd.local' updated
```

### Creating Apps Via CLI[

First we need to set the current namespace to argocd running the following command:
```
kubectl config set-context --current --namespace=argocd
```

Create the example guestbook application with the following command:
```
argocd app create guestbook --repo https://github.com/argoproj/argocd-example-apps.git --path guestbook --dest-server https://kubernetes.default.svc --dest-namespace default
```

```bash
$ argocd app sync guestbook
$ argocd app get guestbook
gouse@gouse:~/DevOps/multipass_scripts$ argocd app get guestbook
{"level":"warning","msg":"Failed to invoke grpc call. Use flag --grpc-web in grpc calls. To avoid this warning message, use flag --grpc-web.","time":"2025-06-30T22:47:38+03:00"}
{"level":"warning","msg":"Failed to invoke grpc call. Use flag --grpc-web in grpc calls. To avoid this warning message, use flag --grpc-web.","time":"2025-06-30T22:47:38+03:00"}
Name:               argocd/guestbook
Project:            default
Server:             https://kubernetes.default.svc
Namespace:          default
URL:                https://argocd.local/applications/guestbook
Source:
- Repo:             http://192.168.100.5:3000/gouse/argocd-example-apps.git
  Target:           HEAD
  Path:             guestbook
SyncWindow:         Sync Allowed
Sync Policy:        Manual
Sync Status:        Synced to HEAD (f58c7ed)
Health Status:      Healthy

GROUP  KIND        NAMESPACE  NAME          STATUS  HEALTH   HOOK  MESSAGE
       Service     default    guestbook-ui  Synced  Healthy        service/guestbook-ui created
apps   Deployment  default    guestbook-ui  Synced  Healthy        deployment.apps/guestbook-ui created

```

