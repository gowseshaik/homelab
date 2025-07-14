## 🧾 Example Use Case
- 1. You created a volume called `manual-volume` in Longhorn UI
- 2. You now want to mount it to a Pod

Create a `PersistentVolume` and `PersistentVolumeClaim` using `longhorn-static`:
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: manual-pv
spec:
  capacity:
    storage: 2Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: longhorn-static
  csi:
    driver: driver.longhorn.io
    volumeHandle: manual-volume # <-- This must match the volume name in Longhorn UI
    fsType: ext4
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: manual-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi
  storageClassName: longhorn-static
  volumeName: manual-pv
```

🔍 How to List Existing Longhorn Volumes
```shell
kubectl -n longhorn-system exec -it <longhorn-manager-pod> -- longhorn ls
```

Or view via **Longhorn UI** → `Volumes` tab → copy volume name to use in `volumeHandle`.

