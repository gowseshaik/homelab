<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

| Field                    | What it Does                                                           | Common Values                                                                                                                           |
| ------------------------ | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **reclaimPolicy**        | Tells Kubernetes what to do with the actual disk when you delete a PVC | • `Delete` – also deletes the PV and its data• `Retain` – keeps the PV and data for manual cleanup                                      |
| **volumeBindingMode**    | Controls when Kubernetes assigns a PV to a PVC                         | • `Immediate` – binds as soon as PVC is created• `WaitForFirstConsumer` – waits until a pod uses the PVC, so PV lands on the right node |
| **allowVolumeExpansion** | Lets you grow the size of a volume after the PVC is already created    | • `true` – you can increase PVC’s storage size• `false` – size is fixed once PVC is made                                                |
- **Use `Delete`** reclaimPolicy if you want cleanup to happen automatically.
- **Use `WaitForFirstConsumer`** bindingMode for StatefulSets or multi-zone clusters so the volume shows up on the pod’s node.
- **Set allowVolumeExpansion to `true`** if you expect to need more space later.

✅ **Yes**, you can attach and use **multiple StorageClasses** in your K3s cluster.

Kubernetes (and K3s) fully support **multiple StorageClasses**, and you can pick the right one per PVC using the `storageClassName` field.

## 🔧 How It Works
- You can install multiple **CSI drivers** (like Longhorn, NFS, Ceph, etc.).
- Each driver typically registers its own **StorageClass**.
- You choose which StorageClass to use **per PVC**.

## 🧠 Example: Using Multiple StorageClasses

### 1. **List all StorageClasses**
```bash
kubectl get storageclass
```

Example output:
```
NAME             PROVISIONER             DEFAULT
local-path       rancher.io/local-path   yes
longhorn         driver.longhorn.io      no
nfs-client       nfs.csi.k8s.io          no
```

### 2. **Use Specific StorageClass in Your PVC**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-volume
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: longhorn
```

You can change `storageClassName` to `nfs-client`, `local-path`, etc.

## ⚙️ How to Add a New StorageClass

|Backend|Install Guide|
|---|---|
|**Longhorn**|`helm install` or official YAML|
|**NFS**|Install NFS CSI driver and create StorageClass|
|**Ceph/Rook**|Deploy Rook operator and Ceph cluster|
|**HostPath (custom)**|Manually create PVs + StorageClass|
|**iSCSI, OpenEBS, etc.**|Install respective CSI drivers|
## 📌 Optional: Change the Default StorageClass

```bash
# Set Longhorn as default
kubectl patch storageclass longhorn -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

# Remove default from local-path
kubectl patch storageclass local-path -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'
```

## 🧠 Best Use Case Examples

| App                | Recommended StorageClass           |
| ------------------ | ---------------------------------- |
| MySQL / PostgreSQL | `longhorn` (replication, snapshot) |
| Static website     | `nfs-client` (read-only shared)    |
| Temp processing    | `local-path` (fast, ephemeral)     |
**Mostly the same steps apply to Kubernetes (k8s)** as well, but there are a few key differences between **K3s and standard K8s** you need to be aware of when working with **StorageClasses** and CSI drivers.

## ✅ What’s the Same (K3s vs. K8s)

| Task                                         | Same in K3s & K8s? | Notes                                     |
| -------------------------------------------- | ------------------ | ----------------------------------------- |
| Multiple StorageClasses                      | ✅                  | Use `storageClassName` in PVC             |
| Setting default class                        | ✅                  | Use patch on annotation                   |
| Installing CSI drivers (Longhorn, NFS, etc.) | ✅                  | Helm/YAML-based, works in both            |
| Creating/Binding PVCs                        | ✅                  | Same syntax in YAML                       |
| Velero + CSI Snapshots                       | ✅                  | Requires CSI plugin + VolumeSnapshotClass |
## ⚠️ What’s Different (K3s vs. Full K8s)

|Feature|K3s|K8s|
|---|---|---|
|**Default StorageClass**|`local-path`|Often none (or GCE/AWS default)|
|**Pre-installed CSI drivers**|`local-path-provisioner` only|None (must install manually)|
|**Kubelet root path**|`/var/lib/rancher/k3s`|`/var/lib/kubelet`|
|**CRDs (CSI snapshot, etc.)**|Might not be present|Needs to be installed manually too|
|**Component Management**|Bundled into single binary|Modular (API, controller, etc.)|

## 🧱 Example Differences
### 📦 In K3s:
- You already have a `local-path` StorageClass
- You might already have embedded controller support
- Easier to deploy Longhorn with one Helm chart
### 📦 In K8s (Vanilla):
- You must install a default StorageClass yourself
- Some CRDs (like `volumesnapshotclass`) might be missing
- CSI drivers require RBAC, webhook, snapshot-controller setup
## 🧰 Installation Nuances

|CSI Driver|K3s|K8s|
|---|---|---|
|Longhorn|✅ Helm with built-in defaults|✅ Helm, but ensure `defaultStorageClass` is manually set|
|NFS|✅ Easy if NFS server reachable|✅ Same|
|Ceph/Rook|✅ Works but heavy|✅ Designed for full K8s clusters|
|Velero|✅ Works out of the box if CSI plugin used|✅ Same, but might need manual snapshot-controller install|
## 🔚 Final Verdict

|Scenario|Recommendation|
|---|---|
|Want same behavior on both?|Use CSI-based StorageClass and test PVC binding|
|Need advanced features (e.g., replication, off-node backup)?|Use Longhorn or Ceph with CSI|
|Working across clusters?|Use Velero with CSI snapshot for cross-cluster portability|
