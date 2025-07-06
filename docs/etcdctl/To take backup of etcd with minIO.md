<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
No, **MinIO is _not mandatory_** — it's just a **self-hosted S3-compatible storage**. But it's an **excellent choice** for storing etcd backups **on-prem** or in air-gapped clusters.

---
### ✅ When You Need MinIO

You need MinIO **only if**:

- You don’t have AWS/GCS/S3 already.
- You want **local S3-compatible storage** inside Kubernetes.
- You use tools like Stash, Velero, kube-etcd-backup expecting S3.

### 🛠️ How to Setup MinIO on Kubernetes (Simple & Persistent)

#### 1. **Create Namespace**
```bash
kubectl create namespace minio
```
#### 2. **Apply MinIO Deployment & PVC**
```yaml
# minio-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: minio
  namespace: minio
spec:
  replicas: 1
  selector:
    matchLabels:
      app: minio
  template:
    metadata:
      labels:
        app: minio
    spec:
      containers:
      - name: minio
        image: quay.io/minio/minio
        args:
        - server
        - /data
        env:
        - name: MINIO_ACCESS_KEY
          value: minioadmin
        - name: MINIO_SECRET_KEY
          value: minioadmin
        ports:
        - containerPort: 9000
        volumeMounts:
        - name: storage
          mountPath: /data
      volumes:
      - name: storage
        persistentVolumeClaim:
          claimName: minio-pvc
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: minio-pvc
  namespace: minio
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```
```bash
kubectl apply -f minio-deploy.yaml
```
#### 3. **Expose with NodePort (or Ingress)**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: minio
  namespace: minio
spec:
  type: NodePort
  ports:
    - port: 9000
      targetPort: 9000
      nodePort: 30900
  selector:
    app: minio
```

```bash
kubectl apply -f minio-service.yaml
```

Access via:
```
http://<NodeIP>:30900  
User: minioadmin  
Pass: minioadmin
```

### ✅ How to Integrate with Backup Tools

|Tool|Integration with MinIO|
|---|---|
|**Stash**|Add `Repository` CRD with endpoint `http://minio.minio.svc:9000`, and access keys|
|**Velero**|Use `velero install` with `--provider aws --bucket <bucket> --secret-file`|
|**kube-etcd-backup**|Set S3 config with MinIO endpoint & creds|
