<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
### ✅ Prerequisites

|Requirement|Status|
|---|---|
|K3d HA cluster|Already running ✅|
|RWX/RWO filesystem|ext4/xfs (not btrfs)|
|Kernel modules|`open-iscsi` not required inside Docker|
### 🛠️ Steps to Install Longhorn on K3d

#### 1. **Label a node with storage role**
Longhorn needs at least one node to be storage-enabled:

```bash
kubectl label node k3d-ha-cluster-agent-0 longhorn-node=true
```
#### 2. **Install Longhorn using Helm**
```bash
helm repo add longhorn https://charts.longhorn.io
helm repo update

kubectl create namespace longhorn-system

helm install longhorn longhorn/longhorn \
  --namespace longhorn-system \
  --set defaultSettings.createDefaultDiskLabeledNodes=true \
  --set defaultSettings.defaultDataPath="/var/lib/longhorn" \
  --set persistence.defaultClassReplicaCount=1
```
#### 3. **Access Longhorn UI**
Expose it via port-forward:
```bash
kubectl -n longhorn-system port-forward svc/longhorn-frontend 8080:80
```
Open [http://localhost:8080](http://localhost:8080/)

### ⚠️ Note for K3d

By default, K3d agent containers use **Docker volumes**, so Longhorn's block device support is **virtual**. It still works fine for dev/testing.

If Longhorn fails to schedule volumes, check:
```bash
kubectl get nodes -o wide
kubectl get pods -n longhorn-system
```
### ✅ Verify
```bash
kubectl get sc
kubectl get volumes -n longhorn-system
```

Let me know if you want it added to your K3d YAML config or automated as a script.