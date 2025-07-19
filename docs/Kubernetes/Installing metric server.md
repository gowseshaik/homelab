Basic steps to install **Kubernetes Metrics Server** on your cluster:
### ✅ 1. **Download the official components**
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

> This installs `metrics-server` in `kube-system` namespace with default configuration.

### ✅ 2. **Edit Deployment (optional for bare-metal or self-signed clusters)**

If you're running on a local cluster, Minikube, or custom TLS setup, patch the deployment to skip TLS verification:
```bash
kubectl -n kube-system edit deployment metrics-server
```

➡ Add this under `containers.args`:

```yaml
- --kubelet-insecure-tls
- --kubelet-preferred-address-types=InternalIP,Hostname,ExternalIP
```

Then save & exit.

### ✅ 3. **Verify the deployment**

```bash
kubectl get deployment metrics-server -n kube-system
kubectl get apiservice v1beta1.metrics.k8s.io -o yaml
kubectl top nodes
kubectl top pods --all-namespaces
```
