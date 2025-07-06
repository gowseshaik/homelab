<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
# Types of Storage's

| Storage Type       | Description                                                                                                                                                                                   | Example Use Cases                  |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| **Object Storage** | Stores data as _objects_ with metadata and unique IDs, accessed via APIs (like S3). Optimized for large amounts of unstructured data (files, images, backups). Not a traditional file system. | AWS S3, MinIO, Azure Blob Storage  |
| **File Storage**   | Stores data as files in a hierarchical folder structure, accessible via file protocols (NFS, SMB).                                                                                            | Network shares, local file systems |
| **Block Storage**  | Provides raw storage volumes at the block level for use by OS/file systems (like hard drives).                                                                                                | Longhorn, EBS, Persistent Volumes  |

| Feature         | **Block Storage**                   | **File Storage**                      | **Object Storage**                  |
| --------------- | ----------------------------------- | ------------------------------------- | ----------------------------------- |
| **Structure**   | Raw blocks (like a disk)            | Hierarchical (files & folders)        | Flat (objects with metadata)        |
| **Access**      | Low-level (via OS, formatted as FS) | Via file systems (NFS, SMB)           | Via API (HTTP/REST)                 |
| **Use Cases**   | Databases, VMs, OS disks            | Shared drives, home dirs, web servers | Backups, media, logs, cloud apps    |
| **Performance** | High (I/O intensive)                | Medium                                | Variable (depends on use & service) |
| **Scalability** | Limited to volume size              | Limited by FS & protocol              | Highly scalable                     |
| **Examples**    | AWS EBS, GCP PD, Azure Disk         | NFS, SMB, EFS, Azure Files            | S3, Azure Blob, GCP Cloud Storage   |

## Storage Comparison with **When to Use** ?

| Feature         | **Block Storage**                                                                   | **File Storage**                                                       | **Object Storage**                                                                                               |
| --------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Structure**   | Raw blocks, mount as disk                                                           | Files & folders (hierarchical)                                         | Objects with metadata (flat)                                                                                     |
| **Access**      | Low-level, via OS (mount, format)                                                   | NFS, SMB (file share protocols)                                        | REST API, HTTP-based                                                                                             |
| **Use Cases**   | Databases, boot volumes, containers, VMs                                            | Shared directories, CMS, user home folders                             | Backups, archives, logs, media, cloud-native apps                                                                |
| **Performance** | High IOPS, low latency                                                              | Moderate                                                               | Optimized for throughput, not IOPS                                                                               |
| **Scalability** | Limited to disk/volume                                                              | Limited by filesystem                                                  | Highly scalable (petabytes+)                                                                                     |
| **Examples**    | AWS EBS, GCP Persistent Disk, Azure Disk                                            | NFS, AWS EFS, Azure Files                                              | AWS S3, Azure Blob, GCP Cloud Storage                                                                            |
| **When to Use** | - You need fast I/O (DBs) - Requires filesystem - Persistent volume for VMs or Pods | - Shared access between multiple VMs - Classic apps using file systems | - Store unstructured data (images, videos, logs) - Archive or backup with metadata - Internet-accessible content |

# Storage Types with Tools

| Storage Type       | Tools / Solutions                                                                                                                                        |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Block Storage**  | - AWS EBS<br>- Azure Managed Disks<br>- GCP Persistent Disks<br>- OpenEBS<br>- Longhorn<br>- Ceph RBD<br>- iSCSI<br>- LVM                                |
| **File Storage**   | - NFS<br>- SMB/CIFS<br>- AWS EFS<br>- Azure Files<br>- GCP Filestore<br>- GlusterFS- CephFS                                                              |
| **Object Storage** | - AWS S3<br>- Azure Blob Storage<br>- GCP Cloud Storage<br>- MinIO<br>- Ceph Object Gateway (RGW)<br>- OpenIO<br>- Scality<br>- IBM Cloud Object Storage |
# Kubernetes CSI Drivers (with CLI Tools)

| Storage Type       | Tools / CSI Driver                                                                                        | CLI / Setup Tool                                                                               | Notes                                               |
| ------------------ | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| **Block Storage**  | - `ebs.csi.aws.com` - `pd.csi.storage.gke.io` - `disk.csi.azure.com` - `longhorn.io` - `openebs.io/local` | - `aws eksctl`, `helm` - `gcloud container clusters` - `az aks`, `kubectl` - `helm`, `kubectl` | Use `PersistentVolume` + `StorageClass`             |
| **File Storage**   | - `efs.csi.aws.com` - `file.csi.azure.com` - `nfs.csi.k8s.io` - `cephfs.csi.ceph.com`                     | - `aws cli`, `helm` - `az cli`, `helm` - `kubectl`, custom NFS server - `rook-ceph`, `helm`    | Great for shared file systems                       |
| **Object Storage** | - `s3-csi-driver` (community) - `minio` - `ceph-rgw`                                                      | - `mc` (MinIO client) - `rclone`, `s5cmd`, `aws cli` - `helm`, `rook`                          | Object storage not used as native PV, used via apps |
# Example (EBS CSI - block storage)

```
# Install AWS EBS CSI Driver (EKS example)
kubectl apply -k "github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable/?ref=master"

# StorageClass example
kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-sc
provisioner: ebs.csi.aws.com
parameters:
  type: gp2
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
EOF
```

