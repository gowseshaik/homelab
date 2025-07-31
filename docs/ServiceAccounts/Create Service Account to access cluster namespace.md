To create a `ServiceAccount` and give it access to multiple **kind** clusters, follow these steps:

---

### ✅ Step-by-step (for each cluster)

#### 1. **Create the ServiceAccount**

```bash
kubectl create serviceaccount myadmin-sa -n kube-system
```

#### 2. **Create a ClusterRoleBinding (full access)**

```bash
kubectl create clusterrolebinding myadmin-sa-binding \
  --clusterrole=cluster-admin \
  --serviceaccount=kube-system:myadmin-sa
```

#### 3. **Get the Token for the ServiceAccount**

```bash
SECRET_NAME=$(kubectl get sa myadmin-sa -n kube-system -o jsonpath='{.secrets[0].name}')
kubectl get secret $SECRET_NAME -n kube-system -o jsonpath='{.data.token}' | base64 -d
```

Save this token for later use.

#### 4. **Get the Cluster CA and API Server**

```bash
kubectl config view --minify -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' | base64 -d > ca.crt
kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}'
```

---

### 🔁 Repeat the above for each `kind` cluster:

You must run steps 1–4 in the context of each cluster (switch context using `kubectl config use-context <context-name>`).

---

### 🔧 Optional: Use the token to create a new kubeconfig

If you want to use the `ServiceAccount` token to authenticate in CI or automation, create a kubeconfig like this:

```bash
kubectl config set-credentials myadmin-user --token=<copied-token>
kubectl config set-cluster kind-cluster1 \
  --server=https://<api-server-url> \
  --certificate-authority=./ca.crt
kubectl config set-context myadmin-context \
  --cluster=kind-cluster1 \
  --user=myadmin-user
kubectl config use-context myadmin-context
```

Let me know if you want a script to auto-generate this.