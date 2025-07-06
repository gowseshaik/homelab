<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
### Typical setup steps:

1. Create kind cluster.
2. Deploy MinIO in cluster (or use external S3).
3. Install Velero with MinIO credentials.
4. Create backups and restores.

### Key points for Velero with kind:

- Kind clusters use local Docker volumes, so by default Velero’s object storage backups (like to S3) won’t work without some setup.
    
- You need an object storage backend (e.g., MinIO, AWS S3, or compatible) reachable from the kind cluster for Velero to store backups.
    
- MinIO can be deployed inside the kind cluster as an S3-compatible object store for practicing Velero.
    
- Velero requires cluster-admin permissions in kind (which you can grant).
    
- Backup storage location and volume snapshot support need configuration.

| Storage Type         | Use case                | Supported by Velero?  |
| -------------------- | ----------------------- | --------------------- |
| Longhorn             | Block storage (PV)      | No (not object store) |
| MinIO                | Object storage (S3 API) | Yes                   |
| AWS S3               | Object storage          | Yes                   |
| Azure Blob           | Object storage          | Yes                   |
| Google Cloud Storage | Object storage          | Yes                   |