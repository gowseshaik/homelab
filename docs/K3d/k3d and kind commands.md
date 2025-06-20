### 🟪 **Kind Admin Commands**

```bash
# Create a cluster
kind create cluster --name demo
kind create cluster --config dev-cluster.yaml

# List clusters
kind get clusters

# Delete cluster
kind delete cluster --name demo

# Get kubeconfig path
kind get kubeconfig-path --name demo

# Load docker image into kind cluster
kind load docker-image myimage:tag --name demo

# Export logs
kind export logs ./logs --name demo
```

---

### 🟩 **K3d Admin Commands**

```bash
# Create a cluster
k3d cluster create demo
ked create cluster --config dev-cluster.yaml

# List clusters
k3d cluster list

# Get kubeconfig
k3d kubeconfig get demo

# Delete cluster
k3d cluster delete demo

# Add new node to cluster
k3d node create new-agent --role=agent --cluster=demo

# Start/Stop cluster
k3d cluster stop demo
k3d cluster start demo

# Load image into k3d cluster
k3d image import myimage:tag -c demo

# List nodes
k3d node list
```

---

Let me know if you want full lifecycle automation or multi-node/HA setup too.