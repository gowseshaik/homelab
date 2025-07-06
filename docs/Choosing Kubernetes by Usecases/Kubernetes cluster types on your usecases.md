<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
choose it wisely.

| **Category**               | **Tool/Platform**                  | **Purpose**                            | **Open Source** |
| -------------------------- | ---------------------------------- | -------------------------------------- | --------------- |
| **Local Dev Clusters**     | Minikube                           | Single-node local testing              | ✅ Yes           |
|                            | Kind (Kubernetes in Docker)        | Runs Kubernetes in Docker containers   | ✅ Yes           |
|                            | K3d                                | Lightweight K3s in Docker              | ✅ Yes           |
|                            | MicroK8s                           | Lightweight snap-based K8s             | ✅ Yes           |
| **Lightweight Clusters**   | K3s                                | Lightweight Kubernetes for edge/IoT    | ✅ Yes           |
| **Managed Cloud Services** | GKE (Google Kubernetes Engine)     | Managed Kubernetes by Google Cloud     | ❌ No            |
|                            | EKS (Elastic Kubernetes Service)   | AWS managed Kubernetes                 | ❌ No            |
|                            | AKS (Azure Kubernetes Service)     | Azure managed Kubernetes               | ❌ No            |
|                            | Oracle OKE                         | Oracle managed Kubernetes              | ❌ No            |
|                            | IBM Cloud Kubernetes               | IBM managed Kubernetes                 | ❌ No            |
| **On-Prem & Hybrid**       | OpenShift (OKD = Open-source base) | Enterprise-ready with CI/CD features   | ✅ (OKD only)    |
|                            | Rancher                            | Cluster management and provisioning    | ✅ Yes           |
|                            | VMware Tanzu                       | Enterprise Kubernetes with vSphere     | ❌ No            |
|                            | Platform9                          | SaaS-managed Kubernetes anywhere       | ❌ No            |
| **Installer Tools**        | kubeadm                            | Manual cluster setup                   | ✅ Yes           |
|                            | Kubespray                          | Ansible-based multi-node cluster setup | ✅ Yes           |
|                            | Kops                               | Production-ready cluster management    | ✅ Yes           |
| **Multi-Cluster Mgmt**     | Anthos                             | Hybrid/multi-cloud by Google           | ❌ No            |
|                            | Fleet (Rancher)                    | GitOps and cluster fleet management    | ✅ Yes           |
| **Specialized Use**        | Amazon EKS Anywhere                | On-prem Kubernetes via AWS             | ❌ No            |
|                            | Red Hat OpenShift Local (CRC)      | Local OpenShift cluster for dev/test   | ❌ No (OKD alt)  |