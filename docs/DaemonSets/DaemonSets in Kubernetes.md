<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
**DaemonSets in Kubernetes:**

|**Aspect**|**Details**|
|---|---|
|**What**|A DaemonSet ensures that a pod runs on **every node** (or specific nodes) in a Kubernetes cluster.|
|**Why**|To run background or **node-specific services**, like log collectors, monitoring agents, or storage plugins, on each node.|
|**When**|Use when a **service must be on all nodes**, such as for metrics collection (Prometheus node exporter), log aggregation (Fluentd), or network daemons (CNI).|
|**How**|Create a DaemonSet YAML with kind: `DaemonSet`, target `nodeSelector` (if needed), and deploy it using `kubectl apply -f`.|

Let me know if you want the YAML example.
Here's a real-time example of a **DaemonSet** that deploys **Fluentd** to collect logs from all nodes and push to a log aggregator:

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: kube-system
spec:
  selector:
    matchLabels:
      name: fluentd
  template:
    metadata:
      labels:
        name: fluentd
    spec:
      tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      containers:
      - name: fluentd
        image: fluent/fluentd:v1.16-1
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

This deploys Fluentd as a pod on **every node**, even masters (due to toleration), and mounts the host logs for collection.

Let me know if you want more such DaemonSet use cases (e.g., node-exporter, antivirus, custom script runner, etc.).

No, **DaemonSets** and **Taints/Tolerations** are related concepts in Kubernetes but serve different purposes. Let me clarify the difference:

---

## **1. DaemonSets vs. Taints/Tolerations**

| Feature | **DaemonSet** | **Taints & Tolerations** |
|---------|-------------|------------------------|
| **Purpose** | Ensures a pod runs on **all (or some) nodes** in a cluster. | **Prevents** pods from running on certain nodes unless they explicitly tolerate the taint. |
| **Use Case** | Deploying cluster-wide services (logging, monitoring, networking). | Reserving nodes for specific workloads (e.g., GPU nodes for ML workloads). |
| **How It Works** | Automatically schedules pods on new nodes. | Nodes **repel** pods unless the pod has a matching toleration. |
| **Example** | `fluentd` (logging agent) running on every node. | A node with `NoSchedule` taint only allows pods that tolerate it. |

---

## **2. How They Work Together**
DaemonSets often use **tolerations** to ensure they can run on **tainted nodes** (e.g., master nodes).

### **Example: DaemonSet with Tolerations**
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: my-daemonset
spec:
  template:
    spec:
      tolerations:
      - key: "node-role.kubernetes.io/master"
        operator: "Exists"
        effect: "NoSchedule"
      containers:
      - name: my-container
        image: nginx
```
- This DaemonSet will run on **all nodes**, including those with the `NoSchedule` taint (like master nodes).

---

## **3. When to Use Each?**

### **Use a DaemonSet When:**
✅ You need a pod (e.g., logging agent, monitoring tool) on **every node**.  
✅ You want Kubernetes to **automatically** deploy pods when new nodes join.  

### **Use Taints/Tolerations When:**
✅ You want to **restrict** certain nodes to only run specific pods (e.g., GPU nodes for AI workloads).  
✅ You need to **protect** critical nodes (e.g., master nodes) from running arbitrary workloads.  

---

## **4. Summary**
- **DaemonSet** = "Run this pod on all (or selected) nodes."  
- **Taints/Tolerations** = "Only run pods on this node if they explicitly accept the taint."  

They **work together**—DaemonSets often include tolerations to bypass taints and ensure they run everywhere.  
