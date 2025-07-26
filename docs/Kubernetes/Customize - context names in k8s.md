Rename Kubernetes context names using this command:
```bash
kubectl config get-contexts
kubectl config rename-context kind-dev-cluster dev-cluster
kubectl config rename-context kind-int-cluster int-cluster
```