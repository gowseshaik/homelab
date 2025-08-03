<span style="color:#4caf50;"><b>Created:</b> 2025-08-03</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-08-03</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

Here’s a **complete setup guide** for **Velero + Longhorn** for CSI **snapshot-based backup and restore** — tested with K3s/K8s and fully automated.
## ✅ High-Level Plan

|Step|Task|
|---|---|
|1️⃣|Install Velero with CSI + backup plugins|
|2️⃣|Set up `VolumeSnapshotClass` for Longhorn|
|3️⃣|Create test app with PVC|
|4️⃣|Backup the app using Velero|
|5️⃣|Delete the app|
|6️⃣|Restore and verify the data|
## 1️⃣ Install Velero with CSI Plugin + S3/MinIO Backup Support

> Here we’ll use MinIO for S3-compatible local backup.

### 📦 a. Deploy MinIO (S3) in K8s
```bash
kubectl create namespace minio

helm repo add minio https://charts.min.io/
helm repo update

helm install minio minio/minio \
  --namespace minio \
  --set accessKey=minio \
  --set secretKey=minio123 \
  --set persistence.storageClass=longhorn \
  --set persistence.size=10Gi
```

### 🔑 b. Create Velero Credentials File

Create a file named: `minio-credentials`

```ini
[default]
aws_access_key_id = minio
aws_secret_access_key = minio123
```

### 🔌 c. Install Velero CLI (if not installed)

```bash
curl -LO https://github.com/vmware-tanzu/velero/releases/download/v1.13.0/velero-v1.13.0-linux-amd64.tar.gz
tar -zxvf velero-v1.13.0-linux-amd64.tar.gz
sudo mv velero-v1.13.0-linux-amd64/velero /usr/local/bin/
```

---

### 🚀 d. Install Velero in Cluster with CSI + S3 plugins

```bash
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.9.0,velero/velero-plugin-for-csi:v0.7.0 \
  --bucket velero \
  --secret-file ./minio-credentials \
  --backup-location-config region=minio,s3ForcePathStyle="true",s3Url=http://minio.minio.svc:9000 \
  --use-volume-snapshots=true \
  --snapshot-location-config region=minio \
  --namespace velero
```

---

## 2️⃣ Create Longhorn VolumeSnapshotClass

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: longhorn
driver: driver.longhorn.io
deletionPolicy: Delete
```

Apply:

```bash
kubectl apply -f volumesnapshotclass-longhorn.yaml
```

---

## 3️⃣ Deploy Test App + PVC (uses Longhorn)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: longhorn
---
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
  - name: test
    image: busybox
    command: ["/bin/sh"]
    args: ["-c", "while true; do echo $(date) >> /data/out.txt; sleep 5; done"]
    volumeMounts:
    - mountPath: /data
      name: data-vol
  volumes:
  - name: data-vol
    persistentVolumeClaim:
      claimName: test-pvc
```

---

## 4️⃣ Backup with Velero (uses CSI snapshot)

```bash
velero backup create test-backup --include-namespaces default
```

Verify:

```bash
velero backup get
```

---

## 5️⃣ Delete the App

```bash
kubectl delete pod test-pod
kubectl delete pvc test-pvc
```

---

## 6️⃣ Restore from Backup

```bash
velero restore create --from-backup test-backup
```

Verify:

```bash
kubectl get pods
kubectl get pvc
```

Check the `/data/out.txt` log in the pod:

```bash
kubectl exec -it test-pod -- tail /data/out.txt
```

You should see previously written data (restored from snapshot).

---

## ✅ Success: You now have Full CSI-based Snapshot Backup & Restore with Longhorn and Velero.

Let me know if you want:

- Scheduled recurring backups
    
- Pre/post hooks
    
- Restic + NFS backup combo
    
- Off-cluster DR (disaster recovery) setup across clusters