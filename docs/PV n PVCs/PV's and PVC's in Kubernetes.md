<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
## What are PersistentVolumes (PVs) and PersistentVolumeClaims (PVCs)?

**PersistentVolumes (PVs)**:
- Cluster-wide storage resources provisioned by administrators
- Represent physical storage (NFS, iSCSI, cloud storage, etc.) in the cluster
- Have a lifecycle independent of any individual Pod
- Can be statically provisioned (pre-created) or dynamically provisioned (on-demand)

**PersistentVolumeClaims (PVCs)**:
- Requests for storage by users/application Pods
- Bind to available PVs that match their requirements
- Act as an abstraction layer between Pods and physical storage
- Are namespaced resources (unlike PVs which are cluster-scoped)

## Why use PVs and PVCs?

1. **Data persistence**: Survive Pod restarts and crashes
2. **Storage abstraction**: Decouple storage configuration from Pod specs
3. **Dynamic provisioning**: Automatically create storage when needed
4. **Resource management**: Control storage allocation and access
5. **Portability**: Same manifest can work across different storage backends
6. **Lifecycle management**: Handle storage reclaim policies (retain, delete, recycle)

## When to use PVs and PVCs?

Use PV/PVC when:
- Your application needs to persist data beyond a Pod's lifecycle
- Multiple Pods need to share the same storage
- You need different access modes (ReadWriteOnce, ReadOnlyMany, ReadWriteMany)
- You want to manage storage separately from application deployments
- You need storage with specific performance characteristics (SSD vs HDD)
- You're running stateful applications (databases, message queues, etc.)

## How to use PVs and PVCs?

### Basic Usage

1. **Static Provisioning** (Admin creates PV first)

```yaml
# PersistentVolume (cluster-admin creates)
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  hostPath:
    path: "/mnt/data"
```

```yaml
# PersistentVolumeClaim (user creates)
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi
```

2. **Dynamic Provisioning** (Automatic PV creation)

```yaml
# StorageClass (cluster-admin creates)
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
```

```yaml
# PVC that triggers dynamic provisioning
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-pvc
spec:
  storageClassName: fast
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
```

3. **Using PVC in a Pod**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
    - name: mycontainer
      image: nginx
      volumeMounts:
      - mountPath: "/usr/share/nginx/html"
        name: my-storage
  volumes:
    - name: my-storage
      persistentVolumeClaim:
        claimName: my-pvc
```

### Advanced Usage

1. **Volume Snapshots**:
```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: my-snapshot
spec:
  volumeSnapshotClassName: csi-aws-vsc
  source:
    persistentVolumeClaimName: my-pvc
```

2. **Raw Block Volumes**:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: block-pvc
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Block
  resources:
    requests:
      storage: 10Gi
```

3. **Volume Expansion** (requires StorageClass to allow it):
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: expandable
provisioner: kubernetes.io/aws-ebs
allowVolumeExpansion: true
```

### Best Practices

1. **Use Dynamic Provisioning** for most cases (simpler management)
2. **Set appropriate reclaim policies**:
   - `Retain`: Keep data after PVC deletion (manual cleanup)
   - `Delete`: Automatically delete storage (be careful with production data)
3. **Use StorageClasses** to abstract storage backend details
4. **Monitor storage usage** to avoid unexpected costs
5. **Consider volume snapshots** for backup strategies
6. **Use volume modes appropriately**:
   - `Filesystem` (default) for most applications
   - `Block` for databases or performance-sensitive apps
7. **Set resource requests/limits** for StatefulSets using PVCs

### Troubleshooting

1. **PVC stuck in "Pending" state**:
   - Check if storage class exists
   - Verify sufficient capacity is available
   - Check provisioner logs

2. **Mount errors**:
   - Verify access modes match between PV and PVC
   - Check if multiple Pods are trying to use ReadWriteOnce

3. **Common commands**:
   ```bash
   # Check PVs and PVCs
   kubectl get pv
   kubectl get pvc --all-namespaces
   
   # Describe resources for details
   kubectl describe pv my-pv
   kubectl describe pvc my-pvc
   
   # Check storage classes
   kubectl get storageclass
   
   # Check events for issues
   kubectl get events --sort-by=.metadata.creationTimestamp
   ```

4. **Access modes**:
   - `ReadWriteOnce` (RWO): Read-write by one node
   - `ReadOnlyMany` (ROX): Read-only by many nodes
   - `ReadWriteMany` (RWX): Read-write by many nodes