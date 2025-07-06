<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
Sure! Here's the final concise documentation on **Using Longhorn with Kind cluster and storage behavior**:
# Using Longhorn Storage with Kind Cluster

## Overview
Kind runs Kubernetes inside Docker containers, providing ephemeral nodes without persistent storage by default. To enable persistent volumes (PV) with dynamic provisioning, you can deploy Longhorn, a distributed block storage solution.

## 1. Default Storage Behavior in Kind
- Pods without PVC use **ephemeral container storage** inside the node container.
- Data is **lost** if pod or node restarts.
- PVC requests without a storage provisioner remain in **Pending** state.
- No auto volume expansion without external storage configured.

## 2. Setting Up Longhorn on Kind
### Prerequisites
- Create a **loopback file** on the host as a fake block device:

```bash
mkdir -p /mnt/longhorn
dd if=/dev/zero of=/mnt/longhorn/longhorn-disk.img bs=1G count=10
losetup -fP /mnt/longhorn/longhorn-disk.img
mkfs.ext4 /dev/loopX  # Replace X with actual loop device number
mount /dev/loopX /mnt/longhorn
```

### Kind Cluster Config with Mounts

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraMounts:
  - hostPath: /mnt/longhorn
    containerPath: /mnt/longhorn
- role: worker
  extraMounts:
  - hostPath: /mnt/longhorn
    containerPath: /mnt/longhorn
```
Create cluster using this config.

### Deploy Longhorn
```bash
kubectl apply -f https://raw.githubusercontent.com/longhorn/longhorn/v1.6.1/deploy/longhorn.yaml
```
Set Longhorn’s default data path to `/mnt/longhorn` in the Longhorn UI or via manifest.
## 3. Storage Usage

|Storage Type|Location|Notes|
|---|---|---|
|Pod ephemeral storage|Inside container FS|Lost on restart|
|PVC with Longhorn|`/mnt/longhorn` on Kind nodes|Persistent, managed by Longhorn|
|PVC without provisioner|PVC stays Pending|No storage provisioned|
## 4. Storage Expansion
- Loopback file size **does NOT auto-expand**.
- To increase storage, manually create and mount a larger loopback file or add new devices.
- Real production environments use real disks/cloud storage which support dynamic expansion.

## 5. Recommendations
- Use Longhorn on Kind **only for dev/test/demo**.
- For production or real HA with persistent storage, use **K3s** or **kubeadm** clusters on VMs with real storage devices.
- Consider using **Ingress controllers** to reduce host port mappings and complexity.
