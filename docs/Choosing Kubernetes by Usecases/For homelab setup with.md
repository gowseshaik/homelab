<span style="color:#4caf50;"><b>Created:</b> 2025-07-01</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
You can **practice Kubernetes with HA (2 control planes + 2 workers)** under **~15 GiB memory** using the tools you listed:

|Tool|Supports HA|Min RAM Use|ETCD Option|Lightweight|Recommended|
|---|---|---|---|---|---|
|**Multipass (raw K8s)**|✔️ (manual)|❌ (>15GiB)|✔️ (manual)|❌|❌|
|**K3s with Multipass**|✔️ (with tweaks)|✅ (~10–12GiB)|✔️ (external or embedded)|✔️|✅ Best|
|**Kind**|❌ (no multi-master easily)|✅ (~6–8GiB)|❌ (uses Docker-in-Docker)|✔️|⚠️ Limited (no HA)|
|**K3s with Docker**|✔️ (complex, not ideal)|❌ (~>14GiB)|✔️|⚠️ (Docker bloat)|❌|
|**k0s**|✔️ (native HA)|✅ (~12GiB)|✔️ (etcd native)|✔️|✅ Good|

### ✅ Recommended Setup:

**Option 1: K3s on Multipass**

- Lightweight
- Native etcd HA support via embedded etcd in K3s
- Low memory footprint
- Easy to automate with cloud-init

**Option 2: k0s**

- Built-in support for HA and etcd
- Lightweight binaries
- Works well on multipass or even docker

### 🛠️ Suggested Resource Plan (RAM Split):

|Node Type|Count|RAM Each|Total|
|---|---|---|---|
|Control Plane|2|2.5 GiB|5 GiB|
|Worker Node|2|2.0 GiB|4 GiB|
|Buffer + Host|-|~5–6 GiB|-|

You’ll stay under 14–15 GiB with either **k3s with multipass** or **k0s**.

Yes, here are **other lightweight options** to set up **Kubernetes with HA (2 control + 2 worker) within 15 GiB** RAM usage:

|Tool/Platform|Supports HA|Memory Use|ETCD Support|Runs On|Comments|
|---|---|---|---|---|---|
|**MicroK8s**|✔️ (manual)|✅ Low (~3–4GiB per node)|✔️ (with `--ha`)|Native or VM|Lightweight and simple|
|**Talos + kubeadm**|✔️ Native|✅ (~2GiB/node)|✔️ Full etcd control|Multipass/VM|Very clean, secure OS|
|**Minikube (w/ KVM)**|❌ (no HA)|❌ (heavy)|❌|Local VM|Not ideal for HA|
|**Flatcar + kubeadm**|✔️ (manual)|✅ (~2–3GiB)|✔️|Multipass/VM|Minimal OS|

---

### ✅ Recommended (if you want alternatives):

#### 1. **MicroK8s with HA mode**

- Use snap: `sudo snap install microk8s --classic`
- Enable HA: `microk8s enable ha-cluster`
- Lightweight and full Kubernetes
- Simple to add/remove nodes

#### 2. **Talos OS with kubeadm**

- OS is minimal and API-only, no SSH
- High security
- Cleanest etcd/k8s setup
- Works well even with multipass or QEMU

