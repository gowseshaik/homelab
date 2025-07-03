### 🔐 **1. Authentication**

| Intent                    | Command                                                                     |
| ------------------------- | --------------------------------------------------------------------------- |
| Login to ArgoCD           | `argocd login <ARGOCD_SERVER> --username admin --password <PWD> --grpc-web` |
| List current context      | `argocd context`                                                            |
| Switch to another context | `argocd login <OTHER_ARGOCD_SERVER>`                                        |
| Current context info      | argocd account get-user-info                                                |
### 🔧 **2. Cluster Management**

|Intent|Command|
|---|---|
|List all known clusters|`argocd cluster list --grpc-web`|
|Add external cluster|`argocd cluster add <CONTEXT_NAME> --grpc-web`|
|Remove a cluster|`argocd cluster rm <SERVER_URL>`|

> _Use `kubectl config get-contexts` to find your kube context name._

### 📦 **3. Application Management**

| Intent                        | Command                                                                                                                          |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Create an application         | `argocd app create <APPNAME> --repo <REPO_URL> --path <CHART_PATH> --dest-server <DEST_SERVER> --dest-namespace <NS> --grpc-web` |
| Delete an app                 | `argocd app delete <APPNAME> --yes --grpc-web`                                                                                   |
| List all apps                 | `argocd app list --grpc-web`                                                                                                     |
| Show app status               | `argocd app get <APPNAME> --grpc-web`                                                                                            |
| Sync (apply latest manifests) | `argocd app sync <APPNAME> --grpc-web`                                                                                           |
| Rollback to previous revision | `argocd app rollback <APPNAME> <REVISION>`                                                                                       |
| Manually refresh app state    | `argocd app refresh <APPNAME> --grpc-web`                                                                                        |
| only logs                     | argocd app logs <APP_NAME>                                                                                                       |
| to get the manifests          | argocd app manifests <APP_NAME> --grpc-web                                                                                       |

### To list ArgoCD apps filtered by **status**
```bash
# Get only Synced apps
argocd app list --grpc-web -o wide | grep Synced

# Get only OutOfSync apps
argocd app list --grpc-web -o wide | grep OutOfSync

# Get only Healthy apps
argocd app list --grpc-web -o wide | grep Healthy

# Get only Degraded apps
argocd app list --grpc-web -o wide | grep Degraded
```

### 🧠 **4. App Sync Policies**

|Intent|Command|
|---|---|
|Set auto sync|`argocd app set <APPNAME> --sync-policy automated --grpc-web`|
|Set manual sync|`argocd app set <APPNAME> --sync-policy none --grpc-web`|
|Enable self-heal (auto repair)|`argocd app set <APPNAME> --self-heal --grpc-web`|
|Disable pruning|`argocd app set <APPNAME> --auto-prune=false --grpc-web`|
### 📁 **5. Repositories**

|Intent|Command|
|---|---|
|List repos|`argocd repo list --grpc-web`|
|Add a new Git repo|`argocd repo add <REPO_URL> --username <USER> --password <PWD> --grpc-web`|
|Remove a repo|`argocd repo rm <REPO_URL>`|
### 🔍 **6. Debug / Logs**

|Intent|Command|
|---|---|
|View app logs (kubectl way)|`kubectl logs -n argocd -l app.kubernetes.io/name=argocd-server`|
|View sync history|`argocd app history <APPNAME> --grpc-web`|
|Show diff|`argocd app diff <APPNAME> --grpc-web`|
Got it — let's go deeper with **real-time, practical `argocd` CLI examples** using `--grpc-web`, with real-world flows in DevOps.

## 🔐 7. **Login with Ingress-Exposed ArgoCD**

```bash
argocd login argocd.yourdomain.com \
  --username admin \
  --password <YOUR_PASSWORD> \
  --insecure \
  --grpc-web
```

> Accessing via `argocd.yourdomain.com` behind ingress that only supports HTTP/1.1
## 🔗 8. **Add External K8s Cluster to ArgoCD**

```bash
argocd cluster add gouse-k3s-cluster \
  --name dev-k3s \
  --grpc-web
```

> `gouse-k3s-cluster` is your kube context name from `kubectl config get-contexts`
## 📦 9. **Create & Sync Application from Git**

```bash
argocd app create gouse-guestbook \
  --repo https://github.com/argoproj/argocd-example-apps.git \
  --path guestbook \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default \
  --sync-policy automated \
  --grpc-web
```
Then manually sync (if auto-sync is off):
```bash
argocd app sync gouse-guestbook --grpc-web
```
## 🔄 10. **Update Sync Policy to Self-Heal & Auto-Prune**

```bash
argocd app set gouse-guestbook \
  --sync-policy automated \
  --self-heal \
  --auto-prune \
  --grpc-web
```
> Ensures ArgoCD keeps the app in the desired state
## 🔍 11. **Diff Between Live and Desired**
```bash
argocd app diff gouse-guestbook --grpc-web
```
> Shows what's different between cluster state and Git
## 🧹 12. **Delete an App (including K8s resources)**
```bash
argocd app delete gouse-guestbook --yes --grpc-web
```
## 🧪 13. **Sync a Specific Revision (Git commit SHA)**
```bash
argocd app sync gouse-guestbook \
  --revision 5aeff4b7f93e1d4c9c... \
  --grpc-web
```
## 🧰 14. **Manage Git Repos**
```bash
argocd repo add https://github.com/gouse-devops/demo.git \
  --username gouse \
  --password <TOKEN_OR_PASS> \
  --grpc-web
```

```bash
argocd repo list --grpc-web
```
## 📜 15. **List All Applications**
```bash
argocd app list --grpc-web
```
## 💬 16. **Watch Real-time App Status**
```bash
watch -n2 "argocd app get gouse-guestbook --grpc-web"
```
> Real-time view like `kubectl get pods -w`
## 🌐 17. **Using ArgoCD Behind Ingress (NGINX Example)**

Your Ingress config must have:
```yaml
nginx.ingress.kubernetes.io/backend-protocol: "HTTP"
nginx.ingress.kubernetes.io/grpc-web: "true"
```
Then `--grpc-web` is mandatory or you’ll hit gRPC errors.

