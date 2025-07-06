
![Kube-API-server-Architechture-Diagram](images/Kube-API-server-Architechture-Diagram.png)

Let's go into **deep-dive explanation** of the diagram, walking you through the **complete internal workflow of Kubernetes from scratch**, including basics of each resource/component being used by kubernetes

## 🧱 1. **What Is Kubernetes?**

Kubernetes (K8s) is an open-source **container orchestration system** that automates:

- **Deployment**
- **Scaling**
- **Networking**
- **Management of containerized applications**

## 🔗 2. **Kubernetes Core Building Blocks**

| Component                    | Role                                                                     |
| ---------------------------- | ------------------------------------------------------------------------ |
| **Pod**                      | Smallest deployable unit in Kubernetes. Contains one or more containers. |
| **Deployment**               | Manages the desired state of pods (replicas, updates, rollback).         |
| **Service**                  | Exposes pods to other services/pods or external traffic.                 |
| **Node**                     | A machine (VM/physical) that runs containerized workloads (pods).        |
| **Kubelet**                  | An agent on each node. Ensures containers are running in a pod.          |
| **Kube-proxy**               | Handles network traffic routing for services/pods on a node.             |
| **etcd**                     | A key-value store that saves the entire cluster state.                   |
| **API Server**               | Central access point for the Kubernetes control plane (REST interface).  |
| **Scheduler**                | Assigns unscheduled pods to suitable nodes.                              |
| **Controller Manager**       | Runs background loops (controllers) that watch and adjust cluster state. |
| **Cloud Controller Manager** | Integrates cloud-specific operations (e.g., load balancers).             |
## ⚙️ 3. **Step-by-Step Explanation of Diagram**

### 🧑‍💻 Step 1: Submit Configuration (YAML)

- A **developer or admin** writes a Kubernetes manifest in YAML.
- This defines a **Pod**, **Deployment**, or other resource.
- The user runs:

    ```bash
    kubectl apply -f app.yaml
    ```
   
- The request hits the **Kubernetes API Server**.
![{69A7335F-2DAF-486C-8B60-0DD83CDAA5A7}.png](docs/images/{69A7335F-2DAF-486C-8B60-0DD83CDAA5A7}.png)
### 📥 Step 2: API Server Receives Request

- The **API Server**:
    - Validates the syntax/schema.
    - Authenticates the user.
    - Authorizes the request (via RBAC).

- If valid, forwards the object to **etcd** (backing store).

### 🧠 Step 3: etcd Stores the Cluster State

- **etcd** stores all the key-value configurations, including the new pod spec.
- It acts like a **source of truth**.
- Every change to the cluster (creating, updating, deleting resources) is recorded here.

### 🔄 Step 4–5: Controllers Detect the Change

- The **Controller Manager** continuously watches etcd.
- It notices a new pod spec and checks if the current state matches the desired state.
- If not, it triggers actions (e.g., create a pod).
![{12236FE0-7B72-4054-9B80-86E6560C67B0}.png](docs/images/{12236FE0-7B72-4054-9B80-86E6560C67B0}.png)
### 📦 Step 6: Scheduler Binds Pod to a Node

- The **Scheduler**:

    - Detects the new unassigned pod.
    - Evaluates all available nodes.
    - Based on resources, taints/tolerations, node selectors, and affinity rules → selects a node.
    - The scheduler updates etcd with node assignment.

### 📤 Step 7: Node Kubelet Watches etcd

- **Kubelet** on the selected node sees a new pod assigned to it.

- It:
    - Pulls the container images (from Docker Hub or private registry).
    - Creates containers using the container runtime (containerd, CRI-O, etc).
    - Starts the pod.
![{58929F8F-D4FD-4F7B-B8D4-08FC574675E1}.png](docs/images/{58929F8F-D4FD-4F7B-B8D4-08FC574675E1}.png)
### 🌐 Step 8–10: Kube-proxy Configures Networking

- **Kube-proxy** sets up:

    - iptables or IPVS rules for service load-balancing.
    - Ensures networking for the pod is in place.
    - Handles traffic routing to/from the pod.

### 🌍 Step 11–12: Internet Access

- If the app needs internet:

    - **NAT / kube-proxy** routes the traffic outside the cluster.
    - The pod can access external services like databases, APIs, etc.
![{A8F2395B-ADE9-4E93-B2B8-948260932F3C}.png](docs/images/{A8F2395B-ADE9-4E93-B2B8-948260932F3C}.png)

## 🧠 4. **Bottom Section: API Server Clustering**

- Shows multiple **API server replicas** (API-1 to API-7) behind a load balancer for **High Availability** (HA).

- Follows **etcd quorum** rule:
    
    - Minimum `n/2 + 1` nodes must be alive to maintain consistency.
    - For 7 API servers: Quorum = 4.

- Helps prevent split-brain scenarios and ensures fault tolerance.

![{E0C131A8-497C-493E-A36A-ED5A2BF6BBF5}.png](docs/images/{E0C131A8-497C-493E-A36A-ED5A2BF6BBF5}.png)]
## 🔁 Summary – Kubernetes Control Plane Data Flow

```
User YAML -> API Server -> ETCD -> Controller Manager -> Scheduler -> Kubelet -> Containers (Pod)
```

## ✅ Summary

|Principle|Kubernetes Implementation|
|---|---|
|**State Machine**|etcd as the consistent, distributed key-value store|
|**Reconciliation Loop**|Controllers continuously watch and reconcile desired vs actual state|
|**Declarative Intent**|YAML files define _what_ you want, not _how_ to do it|
|**Loose Coupling**|Modular architecture (API Server, Scheduler, Kubelet, etc.)|
|**Fault Tolerance by Design**|HA API servers + etcd quorum logic|
|**Idempotency**|Reapplying manifests results in the same outcome|
