### ✅ Steps Overview

1. **Deploy Nexus on your cluster**
2. **Expose Nexus (via NodePort or Ingress)**
3. **Persistent storage (PVC)**
4. **Access Nexus UI & configure repos**
5. **Use Nexus repo in CI/CD or package managers**

### 🐳 Nexus Deployment YAML (Basic)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nexus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nexus
  template:
    metadata:
      labels:
        app: nexus
    spec:
      containers:
      - name: nexus
        image: sonatype/nexus3:latest
        ports:
        - containerPort: 8081
        volumeMounts:
        - name: nexus-data
          mountPath: /nexus-data
        resources:
          limits:
            memory: "2Gi"
            cpu: "1"
      volumes:
      - name: nexus-data
        persistentVolumeClaim:
          claimName: nexus-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: nexus
spec:
  type: NodePort
  ports:
    - port: 8081
      targetPort: 8081
      nodePort: 30081
  selector:
    app: nexus
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nexus-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

### 💡 Access Nexus

- Run: `kubectl port-forward svc/nexus 8081:8081`
- Or: open `http://<NODE_IP>:30081`
- Default credentials: `admin / <get from admin.password file inside container>`

### 🔗 Integration Examples

|Tool|Integration Point|
|---|---|
|Docker|Push/pull from Nexus Docker registry|
|Maven/Gradle|Set Nexus as artifact repo|
|Helm|Host your own Helm chart repo|
|CI/CD (Jenkins/GitLab)|Use Nexus as artifact/image/cache store|
