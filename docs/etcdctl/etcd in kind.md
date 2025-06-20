In a Kind cluster, **etcd runs as a static Pod** inside the **control-plane node**, just like in a real kubeadm-based cluster.

### 🔍 Details:

- The control-plane node in Kind includes:
    - `kube-apiserver`
    - `kube-controller-manager`
    - `kube-scheduler`
    - `etcd`      

These run as static pods defined in:

```
/etc/kubernetes/manifests/
```

### 📍 To inspect etcd:

1. **Enter the control-plane container**:
    ```bash
    docker exec -it dev-cluster-control-plane bash
    ```
    
2. **List static pod manifests**:
    ```bash
    ls /etc/kubernetes/manifests
    ```
    
3. **Check etcd manifest**:
    ```bash
    cat /etc/kubernetes/manifests/etcd.yaml
    ```
    
4. **Check etcd logs**:
    ```bash
    docker logs dev-cluster-control-plane | grep etcd
    ```
    
5. **Use `etcdctl` inside container**:  
    ```bash
    ETCDCTL_API=3 etcdctl \
      --endpoints=https://127.0.0.1:2379 \
      --cacert=/etc/kubernetes/pki/etcd/ca.crt \
      --cert=/etc/kubernetes/pki/etcd/server.crt \
      --key=/etc/kubernetes/pki/etcd/server.key \
      endpoint status --write-out=table
    ```

### 📌 Note:

- Kind uses a **single-node control plane**, so etcd is not HA.
- For testing HA etcd, use **kubeadm with VMs** or **K3s with external etcd**.