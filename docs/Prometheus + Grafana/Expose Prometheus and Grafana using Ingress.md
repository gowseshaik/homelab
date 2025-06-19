Steps **expose Prometheus and Grafana using Ingress** in our **k3d cluster** with a custom `values.yaml`.
### 📄 `values.yaml` (save this as `kube-prometheus-values.yaml`):

```yaml
grafana:
  ingress:
    enabled: true
    annotations:
      nginx.ingress.kubernetes.io/rewrite-target: /
    hosts:
      - grafana.local
    path: /
  adminPassword: "admin"

prometheus:
  ingress:
    enabled: true
    annotations:
      nginx.ingress.kubernetes.io/rewrite-target: /
    hosts:
      - prometheus.local
    path: /

alertmanager:
  ingress:
    enabled: true
    annotations:
      nginx.ingress.kubernetes.io/rewrite-target: /
    hosts:
      - alertmanager.local
    path: /
```

### ⚙️ Setup Steps:

1. **Install ingress controller (if not already):**

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/kind/deploy.yaml
```

2. **Wait for ingress controller to be ready:**

```bash
kubectl get pods -n ingress-nginx -w
```

3. **Install the stack with custom values:**

```bash
helm install kube-prometheus prometheus-community/kube-prometheus-stack -n monitoring -f kube-prometheus-values.yaml
```

4. **Add local DNS entries:**

Add the following lines to your `/etc/hosts`:

```
127.0.0.1 grafana.local prometheus.local alertmanager.local
```

5. **Access UIs:**

- Grafana: [http://grafana.local](http://grafana.local/)
- Prometheus: [http://prometheus.local](http://prometheus.local/)
- Alertmanager: [http://alertmanager.local](http://alertmanager.local/)  
    (Default Grafana login: `admin / admin`)

