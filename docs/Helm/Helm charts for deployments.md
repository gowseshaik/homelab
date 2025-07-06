<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
## 🔧 What is a Helm Chart?

A **Helm chart** is a **packaged Kubernetes application**—like a Docker image but for k8s deployments.

---
## 📦 Helm Chart Structure

```bash
mychart/
├── Chart.yaml          # Chart metadata (name, version, etc.)
├── values.yaml         # Default config values
├── templates/          # Kubernetes YAML templates
│   ├── deployment.yaml
│   ├── service.yaml
│   └── _helpers.tpl    # Template helpers (optional)
```

---
## 🧪 Sample Chart for Nginx Deployment

### 1. Create chart:
```bash
helm create nginx-app
```
### 2. Edit `values.yaml`:
```yaml
replicaCount: 2
image:
  repository: nginx
  tag: latest
service:
  type: ClusterIP
  port: 80
```
### 3. Deploy:
```bash
helm install my-nginx ./nginx-app
```
### 4. Upgrade:
```bash
helm upgrade my-nginx ./nginx-app
```
### 5. Uninstall:
```bash
helm uninstall my-nginx
```
## 🧰 Commands Cheat Sheet

| Task            | Command                               |
| --------------- | ------------------------------------- |
| Create chart    | `helm create <name>`                  |
| Install chart   | `helm install <release> <chart-path>` |
| Upgrade chart   | `helm upgrade <release> <chart-path>` |
| Uninstall chart | `helm uninstall <release>`            |
| Show values     | `helm show values <chart>`            |
| Validate chart  | `helm lint <chart-path>`              |
| Dry-run install | `helm install --dry-run --debug ...`  |
