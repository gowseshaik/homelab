Great — since you have a **k3d HA cluster (3 control-plane nodes)**
you're running **embedded etcd**, and can safely perform etcd backups the k3s way.

### ✅ Prerequisites:

- Embedded etcd is used (since you have 3 servers)
- Backup must be done from **only one server node** (typically `server-0`)
- You can exec into the container or mount volumes

### 🔧 Method 1: Manual Backup via `etcdctl` (inside container)

#### 1. Exec into `server-0`

```bash
docker exec -it k3d-ha-cluster-server-0 sh
```

#### 2. Install etcdctl inside a cluster server-0 container
```
ETCD_VER=v3.5.13
curl -L https://github.com/etcd-io/etcd/releases/download/${ETCD_VER}/etcd-${ETCD_VER}-linux-amd64.tar.gz -o etcd.tar.gz
tar xzf etcd.tar.gz
sudo mv etcd-${ETCD_VER}-linux-amd64/etcdctl /usr/local/bin/

docker cp etcdctl <container_name>:/usr/local/bin/etcdctl
docker cp etcdctl k3d-ha-cluster-server-0:/usr/local/bin/etcdctl

docker exec -it <container_name> chmod +x /usr/local/bin/etcdctl
docker exec -it k3d-ha-cluster-server-0 chmod +x /usr/local/bin/etcdctl
inside docker container
chmod 777 /usr/local/bin/etcdctl
```

#### 3. Set etcd env vars:

```sh
export ETCDCTL_API=3
export K3S_DATA_DIR=/var/lib/rancher/k3s
export ETCDCTL_CACERT="${K3S_DATA_DIR}/server/tls/etcd/peer/ca.crt"
export ETCDCTL_CERT="${K3S_DATA_DIR}/server/tls/etcd/peer/server-client.crt"
export ETCDCTL_KEY="${K3S_DATA_DIR}/server/tls/etcd/peer/server-client.key"
```

#### 3. Run backup command:

```sh
etcdctl snapshot save /tmp/etcd-backup.db
```

#### 4. Exit container and copy file out:

```bash
docker cp k3d-ha-cluster-server-0:/tmp/etcd-backup.db ./etcd-backup.db
```

---

### 🔄 Restore (manually)

Let me know if you want to simulate restore too — restoring etcd involves stopping k3s, wiping old data, restoring snapshot, and starting again.

---

### 🛠️ Optional: Automate backup on host

If you want to regularly backup etcd from outside using a script, I can prepare that too — let me know your storage preference (host folder, S3, etc.).

Would you like a backup+restore shell script next?