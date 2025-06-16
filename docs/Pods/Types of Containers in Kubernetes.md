
| **Type**                 | **Description**                                                      | **Use Cases**                                         | **Example Tools/Workloads**                 |
| ------------------------ | -------------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------- |
| **Standard Containers**  | OCI-compliant containers (Docker, containerd, CRI-O).                | Microservices, web apps.                              | `nginx`, `redis`, custom apps.              |
| **Windows Containers**   | Containers running Windows OS (requires Windows nodes).              | .NET apps, legacy Windows services.                   | IIS, SQL Server on Windows.                 |
| **Init Containers**      | Run before main app containers in a pod for setup tasks.             | DB migrations, config preloading.                     | `alpine` (for setup scripts).               |
| **Sidecar Containers**   | Auxiliary containers running alongside the main app in the same pod. | Logging, monitoring, proxying.                        | `Fluentd`, `Envoy`, `Prometheus exporter`.  |
| **Ephemeral Containers** | Temporary containers for debugging (attached to running pods).       | Troubleshooting without restarting pods.              | `busybox`, `alpine` (for `kubectl debug`).  |
| **Job/CronJob**          | Runs a container to completion (Job) or on a schedule (CronJob).     | Batch processing, backups, reports.                   | Database backups, data processing scripts.  |
| **DaemonSet**            | Runs one instance per node (cluster-wide).                           | Log collectors, node monitoring.                      | `kube-proxy`, `Node Exporter`.              |
| **StatefulSet**          | Manages stateful apps with stable network IDs and storage.           | Databases, distributed storage.                       | `MySQL`, `MongoDB`, `Elasticsearch`.        |
| **GPU-Accelerated**      | Containers requiring GPUs/TPUs (needs node support).                 | AI/ML workloads, video encoding.                      | `TensorFlow`, `PyTorch`.                    |
| **Security-Hardened**    | Containers with extra isolation (sandboxing/VMs).                    | Multi-tenant clusters, untrusted workloads.           | `gVisor`, `Kata Containers`.                |
| **Multi-Container Pods** | Pods with multiple containers sharing network/storage.               | Co-located helper services (e.g., log shipper + app). | `app + Fluentd` sidecar.                    |
| **Serverless (FaaS)**    | Containers deployed as serverless functions (scales to zero).        | Event-driven workloads.                               | `Knative`, `OpenFaaS`, `AWS Lambda on EKS`. |
| **Wasm Containers**      | WebAssembly-based workloads (experimental).                          | Edge computing, lightweight plugins.                  | `wasmtime`, `wasmedge`.                     |
### **Key Notes:**
1. **OCI Runtimes**: Kubernetes now defaults to `containerd` or `CRI-O` (Docker is deprecated but still usable via shims).  
2. **Windows Support**: Requires Windows nodes and compatible images.  
3. **Security**: Use `gVisor`/`Kata` for sandboxing, `PodSecurityPolicy` (or Kyverno/OPA) for restrictions.  
4. **Debugging**: Ephemeral containers allow live troubleshooting without pod restarts.  
