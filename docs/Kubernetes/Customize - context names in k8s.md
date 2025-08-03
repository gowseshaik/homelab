<span style="color:#4caf50;"><b>Created:</b> 2025-08-03</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-08-03</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

Rename Kubernetes context names using this command:
```bash
kubectl config get-contexts
kubectl config rename-context kind-dev-cluster dev-cluster
kubectl config rename-context kind-int-cluster int-cluster
```