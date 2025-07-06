<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
# **Hands-On Demo: Deploying Longhorn on Kubernetes**  

In this demo, we’ll:  
✅ **Install Longhorn** on a Kubernetes cluster  
✅ **Create a Persistent Volume Claim (PVC)**  
✅ **Deploy a MySQL database** using Longhorn storage  
✅ **Test fault tolerance** by killing a pod  
✅ **Take a snapshot & restore**  

---

## **Prerequisites**  
- A running **Kubernetes cluster** (Minikube, K3s, EKS, AKS, etc.)  
- `kubectl` configured  
- Helm (for installation)  

---

## **Step 1: Install Longhorn**  

### **Option A: Using Helm (Recommended)**
```bash
helm repo add longhorn https://charts.longhorn.io
helm repo update
helm install longhorn longhorn/longhorn --namespace longhorn-system --create-namespace
```

### **Option B: Using Kubectl**
```bash
kubectl apply -f https://raw.githubusercontent.com/longhorn/longhorn/v1.5.1/deploy/longhorn.yaml
```

### **Verify Installation**
```bash
kubectl get pods -n longhorn-system
```
✅ Expected Output: All pods should be `Running`.  

---

## **Step 2: Access Longhorn Dashboard**  
Port-forward the UI:  
```bash
kubectl port-forward svc/longhorn-frontend -n longhorn-system 8080:80
```
Now, open **http://localhost:8080** in your browser.  

---

## **Step 3: Create a PersistentVolumeClaim (PVC)**  
Create `mysql-pvc.yaml`:  
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
      storage: 5Gi
```
Apply it:  
```bash
kubectl apply -f mysql-pvc.yaml
```
Check in Longhorn UI → **Volume** tab.  

---

## **Step 4: Deploy MySQL with Longhorn Storage**  
Create `mysql-deployment.yaml`:  
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
        ports:
        - containerPort: 3306
        volumeMounts:
        - name: mysql-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-storage
        persistentVolumeClaim:
          claimName: mysql-pvc
```
Deploy it:  
```bash
kubectl apply -f mysql-deployment.yaml
```
Verify:  
```bash
kubectl get pods
kubectl logs <mysql-pod-name>
```

---

## **Step 5: Test Fault Tolerance**  
### **Simulate a Node/Pod Failure**  
```bash
kubectl delete pod <mysql-pod-name>
```
✅ **Observe:**  
- A new pod starts automatically.  
- Data persists because Longhorn ensures **replicated storage**.  

---

## **Step 6: Take a Snapshot & Restore**  
### **Manual Snapshot via Longhorn UI**  
1. Go to **Volumes** → Select your MySQL volume.  
2. Click **"Take Snapshot"**.  
3. (Optional) **Backup to S3** (if configured).  

### **Restore from Snapshot**  
1. In the UI, select the snapshot → **"Create Standby Volume"**.  
2. Update the MySQL deployment to use the new volume.  

---

## **Step 7: Clean Up**  
```bash
kubectl delete deployment mysql
kubectl delete pvc mysql-pvc
helm uninstall longhorn -n longhorn-system
```

---

## **Conclusion**  
You’ve successfully:  
✔ Deployed **Longhorn** on Kubernetes  
✔ Created a **MySQL database** with persistent storage  
✔ Tested **fault tolerance**  
✔ Used **snapshots & backups**  

🚀 **Next Steps:**  
- Try **cross-cluster replication** for disaster recovery.  
- Integrate with **Rancher** for easier management.  

