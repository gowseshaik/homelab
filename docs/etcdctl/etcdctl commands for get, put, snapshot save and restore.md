```bash
# Set a key
etcdctl put foo "bar"

# Get a key
etcdctl get foo

# Save a snapshot
etcdctl snapshot save /backup/etcd-snapshot.db

# Restore a snapshot
etcdctl snapshot restore /backup/etcd-snapshot.db \
  --data-dir=/var/lib/etcd-restored
```

### ✅ **Basic Setup**

1. **Install etcdctl** (if not already available):
    ```bash
    sudo apt install etcd-client
    ```
    
2. **Access etcd running in Kubernetes** (inside control-plane/master node):
    ```bash
    kubectl exec -n kube-system etcd-<node-name> -c etcd -it -- sh
    ```
    
3. **Set environment for etcdctl** (inside the etcd pod or use with `ETCDCTL_API=3`):
    ```bash
    export ETCDCTL_API=3
    ```

### 📘 **Common etcdctl Commands**

|Task|Command|
|---|---|
|View cluster health|`etcdctl --endpoints=<ep> endpoint health`|
|View cluster members|`etcdctl --endpoints=<ep> member list`|
|Get a key|`etcdctl --endpoints=<ep> get <key>`|
|Put a key|`etcdctl --endpoints=<ep> put <key> <value>`|
|Delete a key|`etcdctl --endpoints=<ep> del <key>`|
|List all keys|`etcdctl --endpoints=<ep> get "" --prefix --keys-only`|
|Snapshot save|`etcdctl --endpoints=<ep> snapshot save snapshot.db`|
|Snapshot status|`etcdctl snapshot status snapshot.db`|
|Restore from snapshot|`etcdctl snapshot restore snapshot.db --data-dir /var/lib/etcd-restored`|

> Replace `<ep>` with `https://127.0.0.1:2379` or proper internal IP.

---

### 🔐 **If TLS is Enabled** (as in kubeadm setup):

```bash
etcdctl \
  --cert=/etc/kubernetes/pki/etcd/peer.crt \
  --key=/etc/kubernetes/pki/etcd/peer.key \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --endpoints=https://127.0.0.1:2379 \
  endpoint health
```

---

Let me know if you want example output, script for backup/restore, or a real-time cluster key scan.