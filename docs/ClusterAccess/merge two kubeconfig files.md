<span style="color:#4caf50;"><b>Created:</b> 2025-07-06</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
Here are the commands to **merge two kubeconfig files** (`k1config` and `k2config`) and use them from another machine:

```bash
# Set your base config (usually your default ~/.kube/config)
export KUBECONFIG=/home/gouse/DevOps/multipass_scripts/k1config:/home/gouse/DevOps/multipass_scripts/k2config

# Merge the configs and write to ~/.kube/config
kubectl config view --flatten > ~/.kube/config
```

### One-liner to merge and apply:

```bash
KUBECONFIG=k1config:k2config kubectl config view --flatten > ~/.kube/config
```

> **Make sure you are in `/home/gouse/DevOps/multipass_scripts` or use absolute paths.**

---

### After merge, check available contexts:

```bash
kubectl config get-contexts
```

### To switch between clusters:

```bash
kubectl config use-context <context-name>
```

> Replace `<context-name>` with the actual name listed in `get-contexts` output.

---

Error:
```bash
ouse@gouse:~/DevOps/multipass_scripts$ k config get-contexts
CURRENT   NAME         CLUSTER      AUTHINFO   NAMESPACE
*         devcluster   devcluster   default    
          prdcluster   prdcluster   default    
gouse@gouse:~/DevOps/multipass_scripts$ k get nodes
E0703 10:19:52.025850   36078 memcache.go:265] couldn't get current server API group list: the server has asked for the client to provide credentials
E0703 10:19:52.036931   36078 memcache.go:265] couldn't get current server API group list: the server has asked for the client to provide credentials
E0703 10:19:52.048468   36078 memcache.go:265] couldn't get current server API group list: the server has asked for the client to provide credentials
E0703 10:19:52.060949   36078 memcache.go:265] couldn't get current server API group list: the server has asked for the client to provide credentials
E0703 10:19:52.073295   36078 memcache.go:265] couldn't get current server API group list: the server has asked for the client to provide credentials
error: You must be logged in to the server (the server has asked for the client to provide credentials)
gouse@gouse:~/DevOps/multipass_scripts$ k config set-context devcluster
Context "devcluster" modified.
gouse@gouse:~/DevOps/multipass_scripts$ k get nodes
E0703 10:20:38.496594   36331 memcache.go:265] couldn't get current server API group list: the server has asked for the client to provide credentials
E0703 10:20:38.503812   36331 memcache.go:265] couldn't get current server API group list: the server has asked for the client to provide credentials
E0703 10:20:38.509652   36331 memcache.go:265] couldn't get current server API group list: the server has asked for the client to provide credentials
E0703 10:20:38.515449   36331 memcache.go:265] couldn't get current server API group list: the server has asked for the client to provide credentials
E0703 10:20:38.522562   36331 memcache.go:265] couldn't get current server API group list: the server has asked for the client to provide credentials
error: You must be logged in to the server (the server has asked for the client to provide credentials)
```

```
multipass exec k3s-dev -- sudo cat /etc/rancher/k3s/k3s.yaml > ~/k3s-dev.yaml
multipass exec k3s-prd -- sudo cat /etc/rancher/k3s/k3s.yaml > ~/k3s-prd.yaml

KUBECONFIG=~/k3s-dev.yaml:~/k3s-prd.yaml
kubectl config view --flatten > ~/.kube/config
chmod 600 ~/.kube/config
```

```
kubectl get nodes
kubectl config use-context k3s-context
```

Use the following `KUBECONFIG` and `kubectl config view --flatten` approach to **append another cluster config** to your existing `~/.kube/config`:

```bash
$ multipass exec k3s-master -- sudo cat /etc/rancher/k3s/k3s.yaml > kubeconfig
KUBECONFIG=~/.kube/config:/home/gouse/multipassKUBEconfigs/kubeconfig

KUBECONFIG=~/.kube/config:/path/to/other/cluster/config 
kubectl config view --flatten > /tmp/merged-kubeconfig && 
mv /tmp/merged-kubeconfig ~/.kube/config
```

### Steps:

1. `KUBECONFIG=~/.kube/config:/path/to/other/cluster/config`  
    – Temporarily sets both config files to be loaded.
    
2. `kubectl config view --flatten`  
    – Merges and removes duplicate references.
    
3. `> /tmp/merged-kubeconfig`  
    – Saves merged output to a temp file.
    
4. `mv ... ~/.kube/config`  
    – Overwrites the current config with the merged one.
    

> You can repeat this for more clusters by adding more `:/path` in the `KUBECONFIG`.