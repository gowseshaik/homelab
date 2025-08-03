<span style="color:#4caf50;"><b>Created:</b> 2025-08-03</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-08-03</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

✅ Yes, you can **easily set up an NFS server on your Ubuntu machine**, and then use it in **K3s or Kubernetes** with the **NFS CSI driver** for dynamic volume provisioning.

#### ❓ Can You Use Longhorn _on top of_ NFS?
**🔴 No — Longhorn does not support NFS as a backend.**  
Longhorn **requires direct block storage** (local SSD/HDD attached to nodes).  
You **cannot map NFS to Longhorn** as storage.

## 🛠️ Step-by-Step: Setup NFS on Ubuntu Local Machine
### ✅ 1. **Install NFS Server**
```bash
sudo apt update
sudo apt install nfs-kernel-server -y
```
### ✅ 2. **Create Shared Directory**
```bash
sudo mkdir -p /srv/nfs/k3s-volumes
sudo chown nobody:nogroup /srv/nfs/k3s-volumes
sudo chmod 777 /srv/nfs/k3s-volumes
```

> This will be your shared volume base.
### ✅ 3. **Export the Directory**
Edit exports file:
```bash
sudo nano /etc/exports
```
Add this line:
```bash
/srv/nfs/k3s-volumes  *(rw,sync,no_subtree_check,no_root_squash)
```
Apply the export:
```bash
sudo exportfs -rav
```
Restart the NFS service:
```bash
sudo systemctl restart nfs-kernel-server
```
### ✅ 4. **Check the NFS is Working**
```bash
showmount -e localhost
```
Expected:
```
Export list for localhost:
/srv/nfs/k3s-volumes *
```
## 🔌 (Optional) Open Firewall

If running firewall:
```bash
sudo ufw allow from <your_k3s_node_ip> to any port nfs
```

## 🚀 Next: Use It in K3s with CSI Driver

Let me know and I’ll give you:

- NFS Client Provisioner setup
- YAML for NFS `StorageClass`
- Sample PVC & Pod using the NFS backend
