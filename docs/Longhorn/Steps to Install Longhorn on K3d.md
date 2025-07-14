<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
### ✅ Prerequisites

|Requirement|Status|
|---|---|
|K3d HA cluster|Already running ✅|
|RWX/RWO filesystem|ext4/xfs (not btrfs)|
|Kernel modules|`open-iscsi` not required inside Docker|
## 🧱 Can Longhorn Be Inside Kubernetes or External?
Excellent question. The answer depends on **how you want to design your storage architecture**. Here's a full breakdown:

|Deployment Mode|Supported?|Description|
|---|---|---|
|✅ **Inside Kubernetes**|✅ **Yes (Default)**|Longhorn runs as a **Kubernetes-native storage system** (pods + CRDs inside your cluster)|
|❌ **Fully external**|❌ **Not supported**|Longhorn **cannot run as a standalone external storage appliance**|
|⚠️ **Hybrid (dedicated storage cluster)**|⚠️ Yes, with advanced config|You can build a **dedicated Longhorn K3s cluster** acting as networked storage for other clusters (via NFS/iSCSI)**|
## ✅ Default: Longhorn **Inside** Your K3s/K8s Cluster
This is the recommended, supported, and most stable setup:
- Longhorn runs in `longhorn-system` namespace
- Each node contributes local disks (e.g., `/var/lib/longhorn`)
- Volumes are created, replicated, snapshotted via Kubernetes APIs
- Integrated with CSI
### Pros:
- Simple, Kubernetes-native
- No external dependencies
- Works with Velero, VolumeSnapshotClass, PVCs
### Example Setup:
```bash
kubectl get pods -n longhorn-system
kubectl get storageclass longhorn
```

## 🧪 Advanced: Dedicated Longhorn Cluster (Hybrid Storage Mode)

You can **run Longhorn in a separate K3s cluster**, and expose volumes to other clusters via:

- **iSCSI** (manual)
- **NFS** (using Longhorn volumes + nfs-provisioner)
- **Restic/NFS for Velero restore/backup**

> But this is **not supported directly by Longhorn** as external storage — it's a workaround.

## ❌ Not Possible: Longhorn as a Pure External Storage Appliance

Unlike Ceph, TrueNAS, or NetApp:
- Longhorn is **not designed to be installed on bare metal or VMs outside Kubernetes**
- It **must run inside a Kubernetes cluster** (even a minimal K3s)

## 🧠 First Insight

|Storage Type|Suitable For|
|---|---|
|Longhorn inside K3s|✅ Most apps, PVCs, CSI, snapshots|
|Longhorn in separate K3s cluster (storage-only)|⚠️ Shared storage for other clusters, requires NFS/iSCSI export|
|External NAS (e.g. NFS, Ceph, SAN)|✅ Multi-cluster, legacy workloads, direct access|
|Longhorn as external appliance|❌ Not supported or intended|

## 🧰 Want to Try: Dedicated Storage K3s Cluster with Longhorn?

If you're interested in running **Longhorn as a storage service** using a separate K3s setup, I can provide:

- Setup steps for `longhorn + nfs-provisioner`
- Export volumes from storage cluster
- Mount them on other K3s clusters via NFS PVC

Let me know if you want that architecture.
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

or

helm install longhorn longhorn/longhorn --namespace longhorn-system
# Verify CSI + StorageClass
kubectl get storageclass
Should show:
NAME       PROVISIONER             DEFAULT
longhorn   driver.longhorn.io      no

# To make longhorn as default:
kubectl patch storageclass longhorn -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

$ kubectl get pods -n longhorn-system

gouse@gouse:~$ k get storageclass
NAME                   PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
local-path (default)   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  8d
longhorn (default)     driver.longhorn.io      Delete          Immediate              true                   4m20s
longhorn-static        driver.longhorn.io      Delete          Immediate              true                   4m17s
```

🧾 What This Means

|Attribute|Value|
|---|---|
|**StorageClass Name**|`local-path`|
|**Provisioner**|`rancher.io/local-path` (default for K3s)|
|**Reclaim Policy**|`Delete` — PVs will be deleted when PVCs are deleted|
|**Binding Mode**|`WaitForFirstConsumer` — volume is not provisioned until Pod is scheduled|
|**Expansion Support**|❌ `false` — PVCs **cannot** be resized dynamically|
|**Default?**|✅ Yes|
## 📦 What is `longhorn-static` StorageClass?

**`longhorn-static`** is a **StorageClass used for statically provisioning** volumes that were **already created manually** in the Longhorn UI or API — i.e., volumes that exist before any PVC binds to them.

|Concept|`longhorn` (dynamic)|`longhorn-static` (static)|
|---|---|---|
|Who creates the volume?|Kubernetes (via PVC)|You (via Longhorn UI, script, etc.)|
|When is it created?|When a PVC is applied|Before PVC exists|
|How is it bound?|PVC → Longhorn creates volume|PVC binds to pre-existing volume|
|Use case|Dynamic workloads|Manual restore, pre-imported disks, migration
## ✅ When to Use `longhorn-static`

You use `longhorn-static` when:

1. You **manually created a volume** in the Longhorn UI  
    (e.g., from a backup, snapshot, or disk import)
2. You want to **bind it to a PVC** inside Kubernetes
3. You **don’t want K8s to create a new volume**, but reuse an existing one

|Concept|Why It Matters|
|---|---|
|CSI = Container Storage Interface|Standard for dynamic volume provisioning across all K8s distros|
|Longhorn/Ceph use CSI drivers|To allow `PersistentVolumeClaim` to dynamically bind to real volumes|
|Works with Velero|For CSI snapshots (backup/restore PVCs)|

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

## How to List Existing Longhorn Volumes
```shell
kubectl -n longhorn-system exec -it <longhorn-manager-pod> -- longhorn ls
```

