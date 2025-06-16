## **1. Understanding Access Modes in Longhorn**
Kubernetes Persistent Volumes (PVs) and Persistent Volume Claims (PVCs) support different **access modes**, which define how volumes can be mounted by pods.

### **Supported Access Modes in Longhorn**
| Access Mode | Description | Use Case |
|-------------|-------------|----------|
| **`ReadWriteOnce` (RWO)** | Only **one pod** (on a single node) can mount the volume in read-write mode. | Single-instance databases (MySQL, PostgreSQL) |
| **`ReadOnlyMany` (ROX)** | **Multiple pods** (across different nodes) can mount the volume in **read-only** mode. | Shared configuration files (e.g., `nginx.conf`) |
| **`ReadWriteMany` (RWX)** | **Multiple pods** (across different nodes) can mount the volume in **read-write** mode. | Shared file storage (NFS-like, e.g., WordPress uploads) |

### **Which Access Modes Does Longhorn Support?**
✅ **Longhorn supports:**  
- `ReadWriteOnce` (RWO) – Default and most stable.  
- `ReadWriteMany` (RWX) – Requires **NFSv4** or **Samba** (experimental).  

❌ **Longhorn does NOT natively support `ReadOnlyMany` (ROX).**  

---

## **2. How to Change Access Modes in Longhorn**
### **Option A: Define in PVC YAML**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
spec:
  accessModes:
    - ReadWriteOnce  # Change to ReadWriteMany for RWX
  storageClassName: longhorn
  resources:
    requests:
      storage: 10Gi
```

### **Option B: Using RWX (ReadWriteMany)**
1. **Enable RWX in Longhorn UI:**  
   - Go to **Settings** → **Enable NFSv4** (or Samba).  
2. **Create an RWX PVC:**  
   ```yaml
   accessModes:
     - ReadWriteMany
   ```

---

## **3. How to Increase or Decrease Volume Size**
### **Option 1: Expand a Volume (Increase Size)**
1. **Edit the PVC:**  
   ```bash
   kubectl edit pvc <pvc-name>
   ```
   Change `storage: 5Gi` → `storage: 20Gi`.  

2. **Verify Expansion in Longhorn UI:**  
   - Go to **Volumes** → Check the new size.  

3. **Resize Filesystem (if needed):**  
   ```bash
   kubectl exec -it <pod-name> -- df -h /var/lib/mysql  # Check current size
   kubectl exec -it <pod-name> -- resize2fs /dev/longhorn/<volume-name>  # For ext4
   ```

### **Option 2: Shrink a Volume (Decrease Size)**
⚠ **Shrinking is risky and not officially supported!**  
- **Workaround:**  
  1. Take a **snapshot**.  
  2. Create a **new smaller volume** and restore data.  
  3. Update the PVC to point to the new volume.  

---

## **4. Real-World Scenarios**
### **Scenario 1: Scaling MySQL Storage**
- **Problem:** MySQL is running out of space.  
- **Solution:**  
  ```bash
  kubectl edit pvc mysql-pvc  # Change 10Gi → 50Gi
  ```
  Longhorn automatically expands the volume.  

### **Scenario 2: Shared Storage for WordPress**
- **Problem:** Multiple WordPress pods need shared uploads.  
- **Solution:**  
  ```yaml
  accessModes:
    - ReadWriteMany  # Uses NFS under the hood
  ```

---

## **5. Best Practices**
✔ **For databases:** Use `ReadWriteOnce` (RWO).  
✔ **For shared files:** Use `ReadWriteMany` (RWX) with NFS.  
✔ **Always take snapshots** before resizing.  
❌ **Avoid shrinking volumes** (data loss risk).  

---

## **Conclusion**
- **Access Modes:**  
  - `RWO` = Single pod (default).  
  - `RWX` = Multi-pod (requires NFS).  
- **Resizing:**  
  - **Increase size** → Edit PVC.  
  - **Decrease size** → Backup & restore to a new volume.  

🚀 **Next Steps:**  
- Try **dynamic volume provisioning** with `storageClassName: longhorn`.  
- Explore **backup & restore** to S3.  

# **Step-by-Step Demo: Resizing Longhorn Volumes in Kubernetes**

## **🔥 What We'll Cover**
1. **Creating a PVC** (5Gi → 20Gi expansion)  
2. **Attaching it to a MySQL Pod**  
3. **Expanding the Volume** (Live resize)  
4. **Shrinking Safely** (Via backup & restore)  

---

# **Step 1: Deploy a Test MySQL Pod with Longhorn PVC**
### **1.1 Create a PVC (`mysql-pvc.yaml`)**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: longhorn
  resources:
    requests:
      storage: 5Gi  # We'll expand this later
```

Apply it:
```bash
kubectl apply -f mysql-pvc.yaml
```

### **1.2 Deploy MySQL (`mysql-deployment.yaml`)**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
spec:
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:5.7
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: "password"
        volumeMounts:
        - name: mysql-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-storage
        persistentVolumeClaim:
          claimName: mysql-pvc
```

Deploy:
```bash
kubectl apply -f mysql-deployment.yaml
```

### **1.3 Verify PVC & Pod**
```bash
kubectl get pvc  # Should show 5Gi
kubectl get pods  # Wait for MySQL to run
```

---

# **Step 2: Expand Volume from 5Gi → 20Gi**
### **2.1 Edit PVC Live**
```bash
kubectl edit pvc mysql-pvc
```
Change:
```yaml
resources:
  requests:
    storage: 20Gi  # Update from 5Gi → 20Gi
```

### **2.2 Verify Expansion in Longhorn UI**
1. Open Longhorn Dashboard:
   ```bash
   kubectl port-forward svc/longhorn-frontend -n longhorn-system 8080:80
   ```
   Visit **http://localhost:8080** → Check volume size.

2. Confirm in Kubernetes:
   ```bash
   kubectl get pvc mysql-pvc  # Should show 20Gi
   ```

### **2.3 Resize Filesystem (If Needed)**
If MySQL doesn’t see the new space:
```bash
# Enter the MySQL pod
kubectl exec -it <mysql-pod-name> -- bash

# Check current disk space
df -h /var/lib/mysql  # Likely still shows 5Gi

# Resize ext4 filesystem (for Longhorn volumes)
resize2fs /dev/longhorn/<volume-name>  # Autocomplete with `ls /dev/longhorn/`

# Verify
df -h /var/lib/mysql  # Now shows 20Gi
```

---

# **Step 3: Safely Shrink Volume (20Gi → 10Gi)**
### **3.1 Take a Snapshot (Longhorn UI)**
1. Go to **Volumes** → Select `mysql-pvc`.  
2. Click **"Take Snapshot"**.  
3. (Optional) **Backup to S3** for disaster recovery.  

### **3.2 Create a New Smaller PVC**
```yaml
# new-mysql-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc-small
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: longhorn
  resources:
    requests:
      storage: 10Gi  # Smaller size
```

Apply:
```bash
kubectl apply -f new-mysql-pvc.yaml
```

### **3.3 Restore Data to New PVC**
1. In Longhorn UI:  
   - Go to **Snapshot** → **"Create Volume"** from snapshot.  
   - Attach it to `mysql-pvc-small`.  

2. Update MySQL Deployment:
   ```bash
   kubectl edit deployment mysql
   ```
   Change:
   ```yaml
   volumes:
   - name: mysql-storage
     persistentVolumeClaim:
       claimName: mysql-pvc-small  # Point to new PVC
   ```

3. Verify:
   ```bash
   kubectl get pvc  # Should show mysql-pvc-small (10Gi)
   kubectl exec -it <mysql-pod> -- df -h /var/lib/mysql  # Should show 10Gi
   ```

---

# **Key Takeaways**
✅ **Expanding is easy:** Just edit PVC → Longhorn handles the rest.  
⚠ **Shrinking is risky:** Requires backup → restore to a new volume.  
🔧 **Always test resizing in staging first!**  

## **Next Steps**
- **Automate snapshots** with Longhorn’s **Recurring Jobs**.  
- Try **RWX volumes** for shared storage (e.g., WordPress).  

Need help with **specific workloads** (PostgreSQL, MongoDB)? Ask away! 🚀