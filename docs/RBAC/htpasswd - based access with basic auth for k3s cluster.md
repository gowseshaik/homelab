<span style="color:#4caf50;"><b>Created:</b> 2025-07-01</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
To set up **user-based access with basic auth (htpasswd)** for your **K3s cluster**, follow this secure and simple approach using the Kubernetes **basic-auth plugin via Ingress (e.g., Traefik)** or directly via **Kubernetes API with RBAC**.

## ❗ Important: K3s does **not** support `--basic-auth-file`

So you **can’t plug in an `htpasswd` file directly** like in upstream `kube-apiserver`.


### ✅ Goal:

- Create admin users with **username/password**
- Use `htpasswd` for basic auth
- Configure **RBAC roles** in Kubernetes
- Allow external `kubectl` access using their credentials

## 🛠️ Step-by-Step Setup

### 🔐 1. **Install `htpasswd` Tool**

On your local machine:

```bash
sudo apt install apache2-utils
```

### 🧑‍💻 2. **Generate User Credentials**

```bash
sudo su # switch to root user and execute

htpasswd -c ./users.htpasswd admin1
# Enter password when prompted

htpasswd ./users.htpasswd admin2
```

This creates `users.htpasswd` like:

```
admin1:$apr1$M9b1Z...     # hashed password
admin2:$apr1$Yx9ZL...
```

### 🚀 3. **Create Kubernetes Secret**

Copy this to `cp1` if needed:

```bash
kubectl create secret generic basic-auth \
  --from-file=auth=users.htpasswd \
  -n kube-system
```

### 🔏 4. **Enable API Server Basic Auth (K3s Only)**

Edit `/etc/systemd/system/k3s.service` on **all control-plane nodes**:

Find the `ExecStart` line, and **append**:

```bash
--basic-auth-file /var/lib/rancher/k3s/server/basic-auth.csv
```

Now create that CSV:

```bash
sudo tee /var/lib/rancher/k3s/server/basic-auth.csv <<EOF
admin1,$apr1$M9b1Z...,admin1,system:masters
admin2,$apr1$Yx9ZL...,admin2,system:masters
EOF
```

> Format: `username,password,user,group`

Restart K3s:

```bash
sudo systemctl daemon-reexec
sudo systemctl restart k3s
```

Repeat for cp2 as well.

### 🛡️ 5. **Create RBAC RoleBinding (if needed)**

If not using `system:masters` (cluster admin), you can assign limited roles:

🛠️ Working Alternative – Static kubeconfig per user
```
sudo cat /etc/rancher/k3s/k3s.yaml > kubeconfig
cp ~/.kube/config admin1-config
```

Edit `admin1-config` like this:
```
users:
- name: admin1
  user:
    username: admin1
    password: mysecurepassword
```

1. **Create a new user kubeconfig** 

```yaml
# admin-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin1-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: User
  name: admin1
  apiGroup: rbac.authorization.k8s.io
```

```bash
kubectl apply -f admin-role.yaml
```

### 🧪 6. **Access Cluster from Host (using new user)**

On the **admin's host** machine, create their kubeconfig:

```bash
cp kubeconfig admin1-config
```

Edit `admin1-config`, replace:

```yaml
users:
- name: default
  user:
    username: admin1
    password: <the password you set>
```

Or dynamically using:

```bash
kubectl config set-credentials admin1 --username=admin1 --password='yourpass'
kubectl config set-context admin1-context --user=admin1 --cluster=default
kubectl config use-context admin1-context
```

Then test:

```bash
KUBECONFIG=admin1-config kubectl get pods --all-namespaces
```
