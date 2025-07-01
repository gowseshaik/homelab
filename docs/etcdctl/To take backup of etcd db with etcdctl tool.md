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

or 
```
ETCD_VER=v3.5.0

# choose either URL
GOOGLE_URL=https://storage.googleapis.com/etcd
GITHUB_URL=https://github.com/etcd-io/etcd/releases/download
DOWNLOAD_URL=${GOOGLE_URL}

rm -f /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz
rm -rf /tmp/etcd-download-test && mkdir -p /tmp/etcd-download-test

curl -L ${DOWNLOAD_URL}/${ETCD_VER}/etcd-${ETCD_VER}-linux-amd64.tar.gz -o /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz
tar xzvf /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz -C /tmp/etcd-download-test --strip-components=1
rm -f /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz

/tmp/etcd-download-test/etcd --version
/tmp/etcd-download-test/etcdctl version
/tmp/etcd-download-test/etcdutl version

mv /tmp/etcd-download-test/etcd /tmp/etcd-download-test/etcdctl /tmp/etcd-download-test/etcdutl /usr/local/bin
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
ETCDCTL API=3 etcdctl \
--endpoints https://172.31.20.211:2379 \
--cacert=/etc/kubernetes/pki/etcd/ca.crt
--cert=/etc/kubernetes/pki/etcd/server.crt
- -key=/etc/kubernetes/pki/etcd/server. keym
snapshot save_snapshot-backup.db

or

etcdctl snapshot save /tmp/etcd-backup.db
```

## Verify Backup

By the way if you not sure about values used in above command then you can check values from your /etc/kubernetes/manifests/etcd.yaml file.  
Let’s confirm status of our backup using,

```
ETCDCTL_API=3 etcdctl --endpoints https://172.17.0.9:2379 snapshot status /tmp/snapshot-backup.db
```

#### 4. Exit container and copy file out:

```bash
docker cp k3d-ha-cluster-server-0:/tmp/etcd-backup.db ./etcd-backup.db
```

### 🔄 Restore (manually)

```
etcdctl restore save /tmp/etcd-backup.db
```

Let me know if you want to simulate restore too — restoring etcd involves stopping k3s, wiping old data, restoring snapshot, and starting again.

### 🛠️ Optional: Automate backup on host

If you want to regularly backup etcd from outside using a script, I can prepare that too — let me know your storage preference (host folder, S3, etc.).

Would you like a backup+restore shell script next?