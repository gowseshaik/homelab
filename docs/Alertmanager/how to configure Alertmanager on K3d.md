### ✅ 1. **Install K3d cluster (if not already)**

```bash
k3d cluster create alert-cluster --agents 2
```

### ✅ 2. **Install Prometheus & Alertmanager with Helm**

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace
```

This deploys:

- Prometheus
- Alertmanager
- Grafana
- Node Exporters

### ✅ 3. **Edit Alertmanager config**

Create a file `alertmanager.yaml` with Gmail SMTP:

```yaml
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'your.email@gmail.com'
  smtp_auth_username: 'your.email@gmail.com'
  smtp_auth_password: 'your_app_password'
  smtp_require_tls: true

route:
  group_by: ['alertname']
  receiver: 'gmail-alert'

receivers:
  - name: 'gmail-alert'
    email_configs:
      - to: 'destination@email.com'
        send_resolved: true
```

### ✅ 4. **Create a Kubernetes Secret for Alertmanager config**

```bash
kubectl -n monitoring create secret generic alertmanager-prometheus-alertmanager \
  --from-file=alertmanager.yaml
```

### ✅ 5. **Restart Alertmanager pod**

```bash
kubectl -n monitoring delete pod -l app.kubernetes.io/name=alertmanager
```

### ✅ 6. **Verify Alertmanager is using the config**

Check via:

```bash
kubectl -n monitoring port-forward svc/prometheus-kube-prometheus-alertmanager 9093
```

Then open: [http://localhost:9093](http://localhost:9093/)

if you want, trigger test alerts also to verify emails.