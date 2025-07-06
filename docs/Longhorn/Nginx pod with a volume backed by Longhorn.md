<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

When you **setup Longhorn in your cluster**, it uses the storage available on the cluster nodes (e.g., the mounted `/mnt/longhorn` directory in Kind) as its **underlying storage pool**.

- Longhorn manages that storage to create **persistent volumes** (block devices).
- It dynamically allocates space from that pool when you create PVCs.
- So, total available storage = sum of the storage Longhorn can access on all nodes (like `/mnt/longhorn`).

|Action|Effect|
|---|---|
|Mount `/mnt/longhorn` on nodes|Provides raw storage space for Longhorn|
|Deploy Longhorn|Manages and exposes block storage volumes|
|Create PVC with Longhorn SC|Allocates storage from Longhorn pool|

```yaml
# longhorn-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: longhorn-pv-demo
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: longhorn
  csi:
    driver: driver.longhorn.io
    fsType: ext4
    volumeHandle: longhorn-pv-demo

---
# longhorn-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: longhorn-pvc-demo
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: longhorn
  volumeName: longhorn-pv-demo

---
# app-with-pvc.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-longhorn-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx-longhorn
  template:
    metadata:
      labels:
        app: nginx-longhorn
    spec:
      containers:
      - name: nginx
        image: nginx:stable
        volumeMounts:
        - name: storage
          mountPath: /usr/share/nginx/html
      volumes:
      - name: storage
        persistentVolumeClaim:
          claimName: longhorn-pvc-demo
```
### Usage:

```bash
kubectl apply -f longhorn-pv.yaml
kubectl apply -f longhorn-pvc.yaml
kubectl apply -f app-with-pvc.yaml
```

Check pod and PVC status:

```bash
kubectl get pvc
kubectl get pv
kubectl get pods
```

---

This deploys an Nginx pod with a volume backed by Longhorn storage mounted at `/usr/share/nginx/html` (serving static content with persistence).  
You can exec into the pod and create files there to verify persistence.