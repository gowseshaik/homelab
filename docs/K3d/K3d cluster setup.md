<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
`k3d` also supports cluster creation using a **YAML config file**, similar to `kind.

---
### ✅ **1. Sample k3d Cluster Config YAML (`k3d-config.yaml`)**
```yaml
apiVersion: k3d.io/v1alpha5
kind: Simple
metadata:
  name: dev-cluster
servers: 1
agents: 2
ports:
  - port: 30907:30907    # Cyclops / Minio
    nodeFilters:
      - loadbalancer
  - port: 31446:31446    # Jenkins
    nodeFilters:
      - loadbalancer
  - port: 31447:31447    # ArgoCD
    nodeFilters:
      - loadbalancer
  - port: 31448:31448    # Gitea
    nodeFilters:
      - loadbalancer
  - port: 30080:80       # Ingress HTTP
    nodeFilters:
      - loadbalancer
  - port: 30443:443      # Ingress HTTPS
    nodeFilters:
      - loadbalancer
  - port: 31000:31000    # Longhorn UI (optional)
    nodeFilters:
      - loadbalancer
  - port: 30090:30090    # Prometheus (optional)
    nodeFilters:
      - loadbalancer
  - port: 30099:3000     # Grafana (optional)
    nodeFilters:
      - loadbalancer
```
### ✅ **2. Create Cluster Using Config**
```
k3d cluster create --config k3d-config.yaml
```
This will expose your services directly on the host ports without needing port-forward. You can add or change ports anytime by editing the config.
