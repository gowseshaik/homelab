Follow these steps:

## ✅ Steps to Access K3s Cluster from Host

### 1. **Copy kubeconfig from the primary node**

You already did this in the script:

```bash
multipass exec cp1 -- sudo cat /etc/rancher/k3s/k3s.yaml > kubeconfig
```

### 2. **Update server IP in kubeconfig**

Replace `127.0.0.1` with the actual IP of `cp1`:

```bash
CP1_IP=$(multipass info cp1 --format json | jq -r '.info["cp1"].ipv4[0]')
sed -i "s/127.0.0.1/${CP1_IP}/g" kubeconfig
```

### 3. **Set KUBECONFIG environment variable**

```bash
export KUBECONFIG=$PWD/kubeconfig
```

### 4. **Test access from host**

```bash
kubectl get nodes
```

You should see:

```
NAME      STATUS   ROLES                  AGE   VERSION
cp1       Ready    control-plane,master   5m    v1.xx.x
cp2       Ready    control-plane,master   4m    v1.xx.x
worker1   Ready    <none>                 3m    v1.xx.x
worker2   Ready    <none>                 3m    v1.xx.x
```

✅ Done — you're now accessing the HA cluster from your **Ubuntu host directly**.

