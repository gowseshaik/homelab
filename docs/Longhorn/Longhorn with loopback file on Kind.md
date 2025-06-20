### 📦 W3H: **Longhorn on Kind**

### 🔹 What:
Run [Longhorn](https://longhorn.io) (distributed block storage for Kubernetes) on a **Kind cluster**.

### 🔹 Why:
To **test or demo** Longhorn in a local Kubernetes environment using containers (Kind) without provisioning real disks or cloud block storage.

### 🔹 When:
Use only for:

- **Dev/test/demo**
- Learning how Longhorn works
- CI/CD pipeline checks (not real performance)

🛑 **Not for production** due to limitations of Kind (runs in Docker, lacks real disks).

### 🔹 How:

|Step|Description|
|---|---|
|1.|**Create loopback file** as fake disk on host|
|2.|**Mount it into Kind node(s)** via `extraMounts`|
|3.|**Deploy Longhorn** using Helm or manifest|
|4.|**Use StorageClass** from Longhorn for PVCs|

### Example: loopback setup for Kind

#### Create loop disk:

```bash
mkdir -p /mnt/longhorn
dd if=/dev/zero of=/mnt/longhorn/longhorn-disk.img bs=1G count=10
losetup -fP /mnt/longhorn/longhorn-disk.img
mkfs.ext4 /dev/loopX  # replace X with correct loop number
mount /dev/loopX /mnt/longhorn
```

#### Kind config:

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

#### Deploy Longhorn:

```bash
kubectl apply -f https://raw.githubusercontent.com/longhorn/longhorn/v1.6.1/deploy/longhorn.yaml
```

> Set `defaultDataPath: /mnt/longhorn` in Longhorn settings.

