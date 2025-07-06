<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
Here's the **most efficient way** to set up **Prometheus + Grafana** for our **Kubernetes K3d cluster** using `kube-prometheus-stack` Helm chart.
### ✅ Prerequisites:

- k3d cluster running
- kubectl configured
- Helm installed

### ⚙️ Setup Steps (One-liner explanations):

1. **Add Helm repo:**

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts && helm repo update
```

2. **Create monitoring namespace:**

```bash
kubectl create ns monitoring
```

3. **Install kube-prometheus-stack:**

```bash
helm install kube-prometheus prometheus-community/kube-prometheus-stack -n monitoring
```

4. **Wait for all pods to be ready:**

```bash
kubectl get pods -n monitoring -w
```

5. **Port-forward Grafana to access UI:**

```bash
kubectl port-forward svc/kube-prometheus-grafana -n monitoring 3000:80
```

6. **Access Grafana at:**

```
http://localhost:3000
```

7. **Default login:**

```
user: admin
pass: prom-operator
```

### 🎯 Notes:

- Prometheus, Alertmanager, Grafana are all included.
- Predefined dashboards + service discovery work out of the box.
- You can customize values via `--set` or a `values.yaml` file if needed.

