<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
To **confirm the exact Ingress Controller** used in your Kubernetes cluster, follow these steps:
### ✅ **1. Check IngressClass Resource**

```bash
kubectl get ingressclass
```
Output example:
```
NAME             CONTROLLER                   ...
nginx            k8s.io/ingress-nginx         ...
traefik          traefik.io/ingress-controller ...
```
### ✅ **2. Describe the Active IngressClass**
```bash
kubectl describe ingressclass <name>
```

Look for the `controller:` field. It tells you which controller manages it.

---
### ✅ **3. Verify the Ingress Controller Deployment**

Use the controller name from above to filter pods:
```bash
kubectl get pods --all-namespaces | grep ingress
```

Or more specifically:
```bash
kubectl get deployments --all-namespaces | grep ingress
```

Look for deployments like:

- `ingress-nginx-controller`
- `traefik`
- `istio-ingressgateway`
---
### ✅ **4. Confirm by Ingress Resource**
```bash
kubectl get ingress -A
```
Then:
```bash
kubectl describe ingress <name> -n <namespace>
```
Check if it refers to a specific `ingressClassName`.
