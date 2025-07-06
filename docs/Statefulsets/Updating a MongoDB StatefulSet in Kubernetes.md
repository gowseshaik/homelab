<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

Updating a **MongoDB StatefulSet** in Kubernetes requires careful handling since StatefulSets manage stateful applications with persistent data. Below is a step-by-step guide on how to **safely apply changes** (e.g., configuration, image version, or resource limits) without causing downtime or data corruption.

---
## **🔧 Steps to Update a MongoDB StatefulSet**
### **1️⃣ Identify the Change Needed**
Possible changes:
- **Configuration** (e.g., `mongod.conf` settings)
- **Docker Image Version** (e.g., `mongo:4.4` → `mongo:5.0`)
- **Resource Limits** (CPU/Memory)
- **Replica Count** (Scaling up/down)
---
### **2️⃣ Update Strategy Options**
StatefulSets support **two update strategies**:

| Strategy | Behavior | Best For |
|----------|----------|----------|
| **RollingUpdate (Default)** | Updates Pods **one by one** (in reverse order: `mongo-2` → `mongo-1` → `mongo-0`) | Minor changes (e.g., configs, non-breaking image updates) |
| **OnDelete** | Requires **manual deletion** of Pods for updates | Major changes (e.g., MongoDB major version upgrade) |

---
### **3️⃣ Example: Updating MongoDB Configuration**
#### **Step 1: Modify the StatefulSet YAML**
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mongo
spec:
  updateStrategy:
    type: RollingUpdate  # Default (Pod-by-Pod replacement)
  template:
    spec:
      containers:
      - name: mongo
        image: mongo:5.0  # Updated image
        env:
        - name: MONGO_INITDB_ROOT_USERNAME
          value: admin
        - name: MONGO_INITDB_ROOT_PASSWORD
          value: password
        volumeMounts:
        - name: mongo-config
          mountPath: /etc/mongod.conf  # Custom config file
  volumeClaimTemplates: [...]
```
#### **Step 2: Apply the Changes**
```sh
kubectl apply -f mongo-statefulset.yaml
```

#### **What Happens?**
- Kubernetes **replaces Pods one by one** (starting from the highest ordinal, `mongo-2` → `mongo-1` → `mongo-0`).
- Each Pod **retains its PVC** (data is preserved).
- The MongoDB replica set **auto-reconfigures** (if properly set up).

---
### **4️⃣ Example: Major Version Upgrade (MongoDB 4.4 → 5.0)**
#### **⚠️ Warning: Requires Manual Intervention**
1. **Set `updateStrategy: OnDelete`**
   ```yaml
   spec:
     updateStrategy:
       type: OnDelete  # Prevents automatic updates
   ```
2. **Apply the new YAML**
   ```sh
   kubectl apply -f mongo-statefulset.yaml
   ```
3. **Manually Delete Pods (One at a Time)**
   ```sh
   kubectl delete pod mongo-2  # Starts with the highest ordinal
   ```
   - Wait for `mongo-2` to rejoin the replica set before deleting the next Pod.

---
### **5️⃣ Verifying the Update**
#### **Check Pod Status**
```sh
kubectl get pods -l app=mongo
```
#### **Check MongoDB Version**
```sh
kubectl exec mongo-0 -- mongosh --eval "db.version()"
```
#### **Check Replica Set Health**
```sh
kubectl exec mongo-0 -- mongosh --eval "rs.status()"
```

---
## **✅ Best Practices for Updating StatefulSets**
1. **Backup Data Before Major Changes**  
   ```sh
   kubectl exec mongo-0 -- mongodump --out /backup
   ```
2. **Test Changes in Staging First**  
3. **Use `RollingUpdate` for Minor Changes**  
4. **Use `OnDelete` for Major Upgrades**  
5. **Monitor Sync Status After Updates**  

---
## **🚨 Common Pitfalls**
- **⚠️ Breaking Replication:** Changing auth credentials without updating all Pods can break sync.
- **⚠️ Downtime Risk:** If `mongo-0` (primary) restarts, a new leader election happens.
- **⚠️ Storage Issues:** Changing `volumeClaimTemplates` does **not** modify existing PVCs.

---

### **Final Answer**
- **For minor changes (configs, patches):** Use `RollingUpdate`.  
- **For major upgrades (MongoDB 4 → 5):** Use `OnDelete` + manual Pod deletion.  
- **Always verify** replica set health after updates.  

