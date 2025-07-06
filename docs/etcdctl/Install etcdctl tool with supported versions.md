<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
Learn etcd : "https://etcd.io/docs/"
```bash
gouse@gouse:~$ k3d version
k3d version v5.8.3
k3s version v1.31.5-k3s1 (default)

gouse@gouse:~$ kubectl version
Client Version: v1.30.4+k3s1
Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
Server Version: v1.31.5+k3s1
```

Since your **k3s version is `v1.31.5-k3s1`**, it uses **etcd v3.5.x** internally.  
✅ So, you should install **`etcdctl v3.5.13`**, which is fully compatible.

---

### 📦 Install `etcdctl v3.5.13` on Host

```bash
ETCD_VER=v3.5.13

wget https://github.com/etcd-io/etcd/releases/download/${ETCD_VER}/etcd-${ETCD_VER}-linux-amd64.tar.gz
tar xzvf etcd-${ETCD_VER}-linux-amd64.tar.gz
sudo mv etcd-${ETCD_VER}-linux-amd64/etcdctl /usr/local/bin/
rm -rf etcd-${ETCD_VER}-linux-amd64*
```

Then confirm:

```bash
etcdctl version
```

---
# etcd compatibility versions list

|Kubernetes Version|etcd Version Used (Bundled)|
|---|---|
|v1.31.x|v3.5.9+|
|v1.30.x|v3.5.9|
|v1.29.x|v3.5.9|
|v1.28.x|v3.5.7|
|v1.27.x|v3.5.6|
|v1.26.x|v3.5.6|
|v1.25.x|v3.5.4|
|v1.24.x|v3.5.3|
|v1.23.x|v3.5.0|
|v1.22.x|v3.4.13|
|v1.21.x|v3.4.13|
|v1.20.x|v3.4.13|
