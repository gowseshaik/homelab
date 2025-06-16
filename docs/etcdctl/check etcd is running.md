```bash
gouse@gouse:~$ etcdctl put foo "bar" {"level":"warn","ts":"2025-06-13T18:12:52.857946+0300","logger":"etcd-client","caller":"v3@v3.5.13/retry_interceptor.go:62","msg":"retrying of unary invoker failed","target":"etcd-endpoints://0xc0005a2000/127.0.0.1:2379","attempt":0,"error":"rpc error: code = DeadlineExceeded desc = latest balancer error: last connection error: connection error: desc = \"transport: Error while dialing: dial tcp 127.0.0.1:2379: connect: connection refused\""} Error: context deadline exceeded
```
The error means `etcdctl` cannot connect to your etcd server at `127.0.0.1:2379`. The connection is refused because etcd is either not running or not listening on that address/port.

Check these:

```bash
# Check if etcd is running
ps aux | grep etcd

# Or if using systemd
sudo systemctl status etcd

# Check if port 2379 is open
ss -tlnp | grep 2379
```

If etcd is not running, start it:

```bash
sudo systemctl start etcd
```

If etcd is running but on a different address/port, set the endpoint explicitly:

```bash
ETCDCTL_API=3 etcdctl --endpoints=<your-etcd-ip>:<port> put foo "bar"
```

# For a k3d cluster
For a **k3d cluster**, etcd runs inside the k3s server container and is not directly accessible on `127.0.0.1:2379` by default.

To interact with etcd in k3d/k3s, you usually:

1. **Exec into the k3s server container** where etcd runs.
    
2. Use etcdctl inside that container with the correct environment variables.
    

Example commands:

```bash
# List k3d containers
docker ps | grep k3d

# Exec into the k3s server container (replace container name)
docker exec -it <k3d-server-container-name> sh

# Inside container, set etcdctl env variables and run command
export ETCDCTL_API=3
export ETCDCTL_ENDPOINTS=https://127.0.0.1:2379
export ETCDCTL_CACERT=/var/lib/rancher/k3s/server/tls/etcd/server-ca.crt
export ETCDCTL_CERT=/var/lib/rancher/k3s/server/tls/etcd/client.crt
export ETCDCTL_KEY=/var/lib/rancher/k3s/server/tls/etcd/client.key

etcdctl put foo "bar"
```

If you want, I can give you the exact command to get your k3d server container name and run etcdctl inside it.

If you **really need etcdctl**, consider:

- Running an etcdctl container inside k3d with mounted certs.
    
- Or use the k3s builtin ==`3s etcd-snapshot`== commands if your version supports it.