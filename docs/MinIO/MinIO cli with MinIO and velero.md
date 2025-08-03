<span style="color:#4caf50;"><b>Created:</b> 2025-08-03</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-08-03</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

The `mc` command is the **MinIO Client** — a command-line tool used to interact with S3-compatible object storage like MinIO.

---

### 🔧 Install `mc` (MinIO Client)

```bash
curl -O https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc
sudo mv mc /usr/local/bin/
```

---

### ✅ Common `mc` Commands

|Command|Description|
|---|---|
|`mc alias set`|Connects `mc` to a MinIO/S3 server|
|`mc mb`|Makes (creates) a new bucket|
|`mc ls`|Lists buckets or contents|
|`mc cp`|Copies files to/from bucket|
|`mc rm`|Removes files or buckets|

---

### 📌 Example for Your Case

```bash
# Connect to your MinIO server
mc alias set local http://172.18.0.1:9001 admin admin123

gouse@gouse:~/DevOps/multipass_scripts$ mc alias set local http://172.18.0.1:9001 admin admin123 mc: <ERROR> Unable to initialize new alias from the provided credentials. S3 API Requests must be made to API port.

The error message indicates you are trying to connect to the **MinIO Console port (`9001`)**, but **`mc` requires the S3 API port**, which by default is **`9000`**, **not `9001`**

# **Start/Verify MinIO server is running with API on port `9000`**:
export MINIO_ROOT_USER=admin
export MINIO_ROOT_PASSWORD=admin123
minio server /data/minio --address ":9000" --console-address ":9001"

# **Then run `mc` against port `9000`**:
mc alias set local http://172.18.0.1:9000 admin admin123


# Create a bucket named "velero"
mc mb local/velero

# List all buckets
mc ls local
```

✅ Perfect! Your MinIO is now correctly connected, and the `velero` bucket is created.

---

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

---

### 📌 After installation

- Check Velero pod:
    

```bash
kubectl get pods -n velero
kubectl logs deployment/velero -n velero
```

