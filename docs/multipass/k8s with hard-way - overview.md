### Why Hardway
Hard disagree because it depends on your goals. Kubernetes the hard way will help you troubleshoot some weird problems with k8s.

🔍 **Core Focus Areas**

| Area                                      | Why It Matters                                                                                |
| ----------------------------------------- | --------------------------------------------------------------------------------------------- |
| **TLS & Certificate Management**          | Learn how security is handled (e.g., etcd, kubelet, apiserver)                                |
| **etcd Cluster Setup**                    | Understand how Kubernetes stores all its state and how consensus works                        |
| **Control Plane Setup**                   | Learn how to manually start and configure `kube-apiserver`, `controller-manager`, `scheduler` |
| **Kubelet + kube-proxy Setup**            | Understand how worker nodes connect to the control plane                                      |
| **Kubeconfig Files**                      | Learn how each component authenticates and communicates                                       |
| **RBAC Configuration**                    | Learn how access control and API authz work in K8s                                            |
| **Networking (Pod CIDRs, Services, DNS)** | Understand pod-to-pod networking and kube-proxy routing                                       |
| **Static Pod Manifest Usage**             | Learn how to run pods without a scheduler on control plane                                    |
| **Manual Cluster Bootstrapping**          | Learn how each component is brought up and talks to the rest                                  |
to install 

### 💡 Goal of Kubernetes the Hard Way

| Goal                   | Description                                                                   |
| ---------------------- | ----------------------------------------------------------------------------- |
| ✅ Learn by Doing       | You manually install and configure every component                            |
| ✅ Understand Internals | See what tools like `kubeadm`, `k3s`, or `kind` actually do behind the scenes |
| ✅ Debugging Skills     | You’ll learn how to debug TLS, kubelet, or API failures manually              |

### ❌ What Not to Focus On

- No need to use `kubeadm`, Helm, or Operators
- Avoid dashboards, metrics, or cloud integrations
- Don’t try to productionize it — this is a learning/lab setup



Yes, you **can install Kubernetes the Hard Way using Multipass**, and it works well for local lab setups.

### ✅ **Why use Multipass?**

- Lightweight Ubuntu VMs
- Easy to create/clone/destroy nodes
- Simulates cloud VMs (Ubuntu LTS)
- No nested virtualization needed (unlike Vagrant/VMware)


### 🧱 **Sample Setup (Multipass VM Layout)**

|VM Name|Role|CPU|RAM|
|---|---|---|---|
|`k8s-lb`|Load Balancer|1|1GB|
|`k8s-master-1`|Controller|2|2GB|
|`k8s-master-2`|Controller|2|2GB|
|`k8s-worker-1`|Worker|2|2GB|
|`k8s-worker-2`|Worker|2|2GB|

### ⚙️ **Step-by-Step with Multipass**

#### 1. **Launch VMs**

```bash
multipass launch --name k8s-lb       --cpus 1 --mem 1G --disk 5G
multipass launch --name k8s-master-1 --cpus 2 --mem 2G --disk 10G
multipass launch --name k8s-master-2 --cpus 2 --mem 2G --disk 10G
multipass launch --name k8s-worker-1 --cpus 2 --mem 2G --disk 10G
multipass launch --name k8s-worker-2 --cpus 2 --mem 2G --disk 10G
```

#### 2. **Get IPs**

```bash
multipass list
```

Save the IPs for `/etc/hosts` and for load balancer config.

#### 3. **Install Dependencies**

SSH into each node:

```bash
multipass shell k8s-master-1
```

Install:

```bash
sudo apt update && sudo apt install -y socat conntrack ipset iptables curl
```

Repeat for all nodes.

#### 4. **Clone and Follow Kubernetes the Hard Way**

From your host:

```bash
git clone https://github.com/kelseyhightower/kubernetes-the-hard-way
cd kubernetes-the-hard-way
```

Then manually execute the steps from that repo, using `multipass exec <vm-name> -- <command>` or `multipass shell`.

---

### 📝 Tip

You can create a `cloud-init` YAML or small setup scripts to automate cert generation or configs. Let me know if you want an example script for this.

Here's a shell script to auto-create and prep VMs for **Kubernetes The Hard Way using Multipass**:

### 🔧 `kthw_multipass_setup.sh`

```bash
#!/bin/bash

# Node specs
MASTER_COUNT=2
WORKER_COUNT=2

# Create load balancer node
multipass launch --name k8s-lb --cpus 1 --mem 1G --disk 5G

# Create controller nodes
for i in $(seq 1 $MASTER_COUNT); do
  multipass launch --name k8s-master-${i} --cpus 2 --mem 2G --disk 10G
done

# Create worker nodes
for i in $(seq 1 $WORKER_COUNT); do
  multipass launch --name k8s-worker-${i} --cpus 2 --mem 2G --disk 10G
done

# Update all nodes and install dependencies
ALL_NODES=(k8s-lb)
for i in $(seq 1 $MASTER_COUNT); do
  ALL_NODES+=(k8s-master-${i})
done
for i in $(seq 1 $WORKER_COUNT); do
  ALL_NODES+=(k8s-worker-${i})
done

echo "📦 Installing dependencies on all nodes..."
for NODE in "${ALL_NODES[@]}"; do
  echo "➡️  ${NODE}"
  multipass exec $NODE -- bash -c "sudo apt update && sudo apt install -y socat conntrack ipset iptables curl"
done

# Get IPs and print them
echo ""
echo "🌐 IP Addresses:"
for NODE in "${ALL_NODES[@]}"; do
  IP=$(multipass info $NODE | grep IPv4 | awk '{print $2}')
  printf "%-15s : %s\n" "$NODE" "$IP"
done

echo ""
echo "✅ Multipass nodes are ready. Proceed with Kubernetes the Hard Way steps."
```

### ✅ Run

```bash
chmod +x kthw_multipass_setup.sh
./kthw_multipass_setup.sh
```

# Here are the **steps to start with** [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)

### 🪜 **Steps to Start with Kelsey Hightower's Repo**

|Step|Description|
|---|---|
|1️⃣|**Clone the Repo**|
|2️⃣|**Read the Prerequisites**|
|3️⃣|**Provision Infrastructure**|
|4️⃣|**Set Env Variables**|
|5️⃣|**Generate Certificates**|
|6️⃣|**Configure etcd**|
|7️⃣|**Setup Control Plane**|
|8️⃣|**Setup Worker Nodes**|
|9️⃣|**Configure Networking**|
|🔟|**Access with kubectl and verify**|

### 🧱 Step-by-Step Commands

#### 1. Clone the repo

```bash
git clone https://github.com/kelseyhightower/kubernetes-the-hard-way.git
cd kubernetes-the-hard-way
```

#### 2. Read prerequisites

Install on your host:

```bash
sudo apt install -y curl unzip
curl -s https://pkg.cfssl.org/R1.2/cfssl_linux-amd64 -o cfssl
curl -s https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64 -o cfssljson
chmod +x cfssl cfssljson
sudo mv cfssl cfssljson /usr/local/bin/
```

Install `kubectl` on host:

```bash
curl -LO https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

#### 3. Setup Multipass nodes (if not done already)

Use the script I gave you earlier.

#### 4. Set environment variables

Edit and export:

```bash
export KUBERNETES_PUBLIC_ADDRESS="<Your-LB-IP>"
export KUBERNETES_CLUSTER_NAME="kubernetes-the-hard-way"
```

#### 5. Follow the repo section-by-section

Inside the repo:

|Section Dir|What It Does|
|---|---|
|`01-prerequisites.md`|Confirm your system and tools|
|`02-certificate-authority.md`|Create CA and TLS certs|
|`03-compute-resources.md`|Setup worker kubelet + kube-proxy|
|`04-certificate-generation.md`|Generate certs for all components|
|`05-kubeconfig-files.md`|Create kubeconfig files|
|`06-data-encryption.md`|Setup encryption config|
|`07-bootstrapping-etcd.md`|Deploy etcd to master nodes|
|`08-bootstrapping-control-plane.md`|Deploy apiserver, controller, scheduler|
|`09-rbac.md`|Configure RBAC and cluster role bindings|
|`10-worker-setup.md`|Deploy kubelet, kube-proxy to workers|
|`11-networking.md`|Setup pod networking (e.g., Calico, Flannel)|
|`12-dns.md`|Deploy CoreDNS|
|`13-smoke-test.md`|Validate cluster is working|

### ✅ Tip

Use `multipass shell <node>` to enter VM and run the commands as-is.

Yes ✅ — you **can automate Kubernetes The Hard Way** setup using **bash scripts** based on the [Kelsey Hightower repo](https://github.com/kelseyhightower/kubernetes-the-hard-way).  
The repo is intentionally manual for learning, but it’s scriptable.

### 🧰 What Can Be Automated?

|Area|Can be Scripted?|Notes|
|---|---|---|
|VM Provisioning (Multipass)|✅ Yes|Already done in earlier script|
|Certificate Generation|✅ Yes|Use `cfssl` and scripts|
|Kubeconfig Files|✅ Yes|Reusable with `kubectl config set-*`|
|etcd + Control Plane Setup|✅ Yes|Use SSH + remote commands|
|Worker Node Bootstrap|✅ Yes|Script `kubelet`, `kube-proxy` installs|
|Networking (Flannel/Calico)|✅ Yes|Apply YAML manifest|
|Testing (kubectl access)|✅ Yes|Final smoke tests via script|

### 🧪 Example Structure for Automation

```bash
kthw-automation/
├── 00-setup-multipass.sh         # Creates all VMs
├── 01-gen-certs.sh               # Certs via cfssl
├── 02-gen-kubeconfigs.sh         # Creates kubeconfig files
├── 03-setup-etcd.sh              # Installs etcd on master nodes
├── 04-setup-control-plane.sh     # Installs kube-apiserver, etc.
├── 05-rbac.sh                    # Admin role binding
├── 06-setup-workers.sh           # Installs kubelet & kube-proxy
├── 07-deploy-networking.sh       # Deploys Flannel/Calico
├── 08-verify-cluster.sh          # Run `kubectl` and test
```

### 🟩 Automation Style

You can either:

- 🔁 Use `multipass exec <node> -- bash -c "<commands>"`, or
    
- 🚀 Use `scp` + `ssh` to copy and run scripts inside VMs

### ⏭️ Next Step

Do you want me to generate the **`01-gen-certs.sh`** and **`02-gen-kubeconfigs.sh`** to start with?  
Or a full end-to-end automation bundle?

Let me know the style: **bash only** or **Ansible**, or **Python fabric** etc.