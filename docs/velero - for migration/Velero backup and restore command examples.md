<span style="color:#4caf50;"><b>Created:</b> 2025-08-03</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-08-03</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

✅ Perfect! Your MinIO is now correctly connected, and the `velero` bucket is created.

### ✅ Now proceed with Velero installation:
```bash
cat <<EOF > credentials-velero
[default]
aws_access_key_id = admin
aws_secret_access_key = admin123
EOF

velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.8.0 \
  --bucket velero \
  --secret-file ./credentials-velero \
  --backup-location-config region=minio,s3ForcePathStyle=true,s3Url=http://172.18.0.1:9000 \
  --use-volume-snapshots=false

```
### 📌 After installation
- Check Velero pod:
```bash
kubectl get pods -n velero
kubectl logs deployment/velero -n velero
```
### ✅ 1. Manual Backup of All Namespaces

```bash
velero backup create full-backup-$(date +%Y%m%d%H%M) --include-namespaces '*' --ttl 168h

gouse@gouse:~/DevOps/multipass_scripts$ velero backup create full-backup-$(date +%Y%m%d%H%M) --include-namespaces '*' --ttl 168h
Backup request "full-backup-202507111054" submitted successfully.
Run `velero backup describe full-backup-202507111054` or `velero backup logs full-backup-202507111054` for more details.

```

- `--ttl 168h`: Backup expiry time (7 days)

### ✅ 2. Backup Specific Namespace

```bash
velero backup create nginx-backup --include-namespaces nginx
```

### ✅ 3. Backup Specific Resources (e.g., deployments only)

```bash
velero backup create only-deployments \
  --include-resources deployments \
  --include-namespaces default
```

### ✅ 4. List All Backups

```bash
velero backup get
```

### ✅ 5. Describe a Backup

```bash
velero backup describe nginx-backup --details
```

### ✅ 6. Restore Full Cluster

```bash
velero restore create full-restore --from-backup full-backup-202507111000
```

### ✅ 7. Restore Specific Namespace

```bash
velero restore create nginx-restore --from-backup nginx-backup \
  --namespace-mappings nginx:nginx-restore
```

### ✅ 8. Delete Backup

```bash
velero backup delete nginx-backup
```

✅ Yes — **Velero stores all backup data in your MinIO bucket** (`velero`) using the **S3 API**.

### 📦 What gets stored in MinIO?

Each backup becomes a folder in the bucket:

```
velero/
└── backups/
    └── nginx-backup/
        ├── backup.json
        ├── pod-volumes/
        └── resources/
```

It includes:

- Kubernetes resource definitions (YAML)
    
- Volume data (if PVCs + Restic/CSI used — you disabled this with `--use-volume-snapshots=false`)

### 🔍 You can verify with:

```bash
mc ls local/velero/backups/
mc tree local/velero/backups/nginx-backup/
```

Or browse `http://172.18.0.1:9001` (MinIO Console) and check the `velero/backups` folder.
