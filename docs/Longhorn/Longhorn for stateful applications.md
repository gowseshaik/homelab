<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

Yes, using **Longhorn for stateful applications** in Kubernetes is a good practice, especially for:

- **Lightweight production or staging clusters**
- **On-prem or edge environments** where cloud storage is unavailable
- **Learning and testing persistent storage**

### Why Longhorn is good for stateful apps:

|Benefits|Details|
|---|---|
|Distributed storage|Replicates data across nodes for fault tolerance|
|Easy management|Web UI + CLI for volume control|
|Dynamic provisioning|Supports PVC creation on demand|
|Snapshot and backup support|Point-in-time data recovery|
|Compatible with Kubernetes|Native CSI driver integration|

### When NOT to use Longhorn:

- Very large-scale or highly performance-sensitive workloads (may need enterprise storage solutions)
- Clusters without enough disk resources or unreliable node storage

### Summary:

|Use case|Recommended?|
|---|---|
|Stateful app on Kind/dev|Yes (for learning/testing)|
|Stateful app on prod Kubernetes|Yes, if nodes have good disks|
|Very high performance storage|Consider other enterprise options|
# You can check existing StorageClasses by running:
```
kubectl get storageclass

root@dev-cluster-control-plane:/# kubectl get storageclass
NAME                 PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
standard (default)   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  46m
```

|Field|What it Does|Common Values|
|---|---|---|
|**reclaimPolicy**|Tells Kubernetes what to do with the actual disk when you delete a PVC|• `Delete` – also deletes the PV and its data• `Retain` – keeps the PV and data for manual cleanup|
|**volumeBindingMode**|Controls when Kubernetes assigns a PV to a PVC|• `Immediate` – binds as soon as PVC is created• `WaitForFirstConsumer` – waits until a pod uses the PVC, so PV lands on the right node|
|**allowVolumeExpansion**|Lets you grow the size of a volume after the PVC is already created|• `true` – you can increase PVC’s storage size• `false` – size is fixed once PVC is made|
- **Use `Delete`** reclaimPolicy if you want cleanup to happen automatically.
- **Use `WaitForFirstConsumer`** bindingMode for StatefulSets or multi-zone clusters so the volume shows up on the pod’s node.
- **Set allowVolumeExpansion to `true`** if you expect to need more space later.

```yaml
# longhorn-storageclass.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: longhorn
provisioner: driver.longhorn.io
reclaimPolicy: Delete
volumeBindingMode: Immediate
allowVolumeExpansion: true

---
# statefulset-with-longhorn.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: nginx-stateful
spec:
  serviceName: "nginx"
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:stable
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: longhorn
      resources:
        requests:
          storage: 5Gi
```

---

### Steps to apply:

```bash
kubectl apply -f longhorn-storageclass.yaml
kubectl apply -f statefulset-with-longhorn.yaml
```

---

### What it does:

- Creates a Longhorn StorageClass that supports dynamic provisioning and volume expansion.
    
- Deploys an Nginx StatefulSet with 3 replicas.
    
- Each pod gets its **own 5Gi Longhorn volume** mounted at `/usr/share/nginx/html`.
    
- Data persists across pod restarts and rescheduling.
    

---

Check PVCs and pods:

```bash
kubectl get pvc
kubectl get pods -l app=nginx
```

---

You can exec into any pod and add files inside `/usr/share/nginx/html` to test persistence.