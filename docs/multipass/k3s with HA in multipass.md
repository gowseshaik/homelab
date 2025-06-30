Here’s a complete **Multipass script** to set up a **Kubernetes HA cluster** using `k3s`, with:

- **2 control plane nodes**
- **2 worker nodes** 
- **Embedded etcd (HA enabled)**

All inside **Multipass VMs**, suitable for your system (15 GiB RAM).

### ✅ Script: `k3s_ha_multipass.sh`

```bash
#!/bin/bash

# Node specs
CPUS=2
DISK=10G
MEM_CP=2G
MEM_WORKER=2G

# Node names
CONTROL_NODES=(cp1 cp2)
WORKER_NODES=(worker1 worker2)
ALL_NODES=("${CONTROL_NODES[@]}" "${WORKER_NODES[@]}")

# 1. Launch VMs
for NODE in "${ALL_NODES[@]}"; do
  multipass launch --name "$NODE" --cpus $CPUS --mem ${MEM_CP} --disk $DISK
done

# 2. Get IPs
for NODE in "${ALL_NODES[@]}"; do
  IP=$(multipass info "$NODE" --format json | jq -r ".info[\"$NODE\"].ipv4[0]")
  echo "$NODE IP: $IP"
done

# 3. Install k3s on first control-plane (cp1)
CP1_IP=$(multipass info cp1 --format json | jq -r '.info["cp1"].ipv4[0]')
multipass exec cp1 -- bash -c "curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC='server --cluster-init' sh -"

# 4. Extract token from cp1
TOKEN=$(multipass exec cp1 sudo cat /var/lib/rancher/k3s/server/node-token)

# 5. Join cp2 to HA cluster
multipass exec cp2 -- bash -c "curl -sfL https://get.k3s.io | K3S_URL=https://${CP1_IP}:6443 K3S_TOKEN=${TOKEN} INSTALL_K3S_EXEC='server' sh -"

# 6. Join worker1 and worker2
for WORKER in "${WORKER_NODES[@]}"; do
  multipass exec $WORKER -- bash -c "curl -sfL https://get.k3s.io | K3S_URL=https://${CP1_IP}:6443 K3S_TOKEN=${TOKEN} sh -"
done

# 7. Fetch kubeconfig to local machine
multipass exec cp1 -- sudo cat /etc/rancher/k3s/k3s.yaml > kubeconfig
sed -i "s/127.0.0.1/${CP1_IP}/g" kubeconfig
echo "Kubeconfig saved to ./kubeconfig"

# 8. Done
echo -e "\n✅ K3s HA cluster setup complete!"
```

### 📝 Notes

- Assumes you have `multipass`, `jq`, and `curl` installed.
- Exposes kubeconfig to access the cluster from your local host.
- Uses **embedded etcd** (HA mode).
- Avoids external load balancer for simplicity (multi-master access via IP).

- MetalLB for load balancing
- ArgoCD / Prometheus on top
- NGINX ingress setup