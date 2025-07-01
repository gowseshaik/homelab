<<<<<<< HEAD
- **1 server node** → uses **SQLite** (default for k3s)  
- **3 or more server nodes** → uses **embedded etcd**
=======
```
k3d cluster create ha-cluster \
  --servers 3 \
  --agents 2 \
  --wait

gouse@gouse:~/DevOps/k3d$ k get nodes
NAME                      STATUS   ROLES                       AGE   VERSION
k3d-ha-cluster-agent-0    Ready    <none>                      35s   v1.31.5+k3s1
k3d-ha-cluster-agent-1    Ready    <none>                      35s   v1.31.5+k3s1
k3d-ha-cluster-server-0   Ready    control-plane,etcd,master   71s   v1.31.5+k3s1
k3d-ha-cluster-server-1   Ready    control-plane,etcd,master   52s   v1.31.5+k3s1
k3d-ha-cluster-server-2   Ready    control-plane,etcd,master   39s   v1.31.5+k3s1
```
>>>>>>> c91f278b3bd9250b0fa8fb946e980dff7cd6132c

```
$ k3d cluster delete ha-cluster

# Traefik ingress disable
$ k3d cluster create ha-cluster \
  --servers 3 \
  --agents 2 \
  --k3s-arg "--cluster-init@server:0" \
  --k3s-arg "--server=https://k3d-ha-cluster-server-0:6443@server:1" \
  --k3s-arg "--server=https://k3d-ha-cluster-server-0:6443@server:2" \
  --k3s-arg "--tls-san=127.0.0.1@server:0" \
  --k3s-arg "--disable=traefik@server:*" \
  --k3s-arg "--disable=metrics-server@server:*" \
  --k3s-arg "--disable-network-policy@server:*" \
  --wait


# Without ingress disable, ingress enable by default by k3d(k3s inside)
$ k3d cluster delete ha-cluster

$ k3d cluster create ha-cluster \
  --servers 3 \
  --agents 2 \
  --k3s-arg "--cluster-init@server:0" \
  --k3s-arg "--server=https://k3d-ha-cluster-server-0:6443@server:1" \
  --k3s-arg "--server=https://k3d-ha-cluster-server-0:6443@server:2" \
  --k3s-arg "--tls-san=127.0.0.1@server:0" \
  --wait
```

$ k3d cluster create --config k3d-etcd-ha.yaml (it wont restart nodes, if host machine restarted)
```
apiVersion: k3d.io/v1alpha5
kind: Simple
metadata:
  name: ha-cluster
servers: 3
agents: 2
options:
  k3s:
    extraArgs:
      - arg: "--cluster-init"
        nodeFilters:
          - server:0
      - arg: "--server=https://k3d-ha-cluster-server-0:6443"
        nodeFilters:
          - server:1
          - server:2
      - arg: "--tls-san=127.0.0.1"
        nodeFilters:
          - server:0
      - arg: "--disable=servicelb"
        nodeFilters:
          - server:*
      - arg: "--disable=metrics-server"
        nodeFilters:
          - server:*
ports:
  - port: 80:80
    nodeFilters:
      - loadbalancer
  - port: 443:443
    nodeFilters:
      - loadbalancer
```

we fixed the cluster to connect without issues by adding 6443 port.

```
apiVersion: k3d.io/v1alpha5
kind: Simple
metadata:
  name: ha-cluster
servers: 3
agents: 2
options:
  k3s:
    extraArgs:
      - arg: "--cluster-init"
        nodeFilters:
          - server:0
      - arg: "--server=https://k3d-ha-cluster-server-0:6443"
        nodeFilters:
          - server:1
          - server:2
      - arg: "--tls-san=127.0.0.1"
        nodeFilters:
          - server:0
      - arg: "--disable=servicelb"
        nodeFilters:
          - server:*
      - arg: "--disable=metrics-server"
        nodeFilters:
          - server:*
ports:
  - port: 80:80
    nodeFilters:
      - loadbalancer
  - port: 443:443
    nodeFilters:
      - loadbalancer
  - port: 6443:6443
    nodeFilters:
      - loadbalancer
```