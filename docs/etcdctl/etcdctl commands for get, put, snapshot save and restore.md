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

