Sharing access to a Kubernetes cluster with other users involves granting them the necessary permissions securely. Below are the steps to achieve this:

---

### **1. Determine the Authentication Method**
Kubernetes supports several authentication methods:
- **kubeconfig File** (Common for external users)
- **Service Accounts** (For apps/automation)
- **Static Token File**
- **OIDC Integration** (For enterprise setups)

For most cases, sharing a **kubeconfig file** (or generating one for the user) is the easiest approach.

---

### **2. Create/Modify a kubeconfig File for the User**
#### **Option A: Share an Existing Admin kubeconfig (Not Recommended for Security)**
- Simply provide the `~/.kube/config` file (contains cluster CA, endpoint, and credentials).
- **Risk:** Grants full cluster access. Use only in trusted environments.

#### **Option B: Generate a Dedicated kubeconfig for the User (Recommended)**
1. **Create a new user certificate/key** (if using TLS auth):
   ```sh
   openssl genrsa -out username.key 2048
   openssl req -new -key username.key -out username.csr -subj "/CN=username/O=group"  # O=group for RBAC
   openssl x509 -req -in username.csr -CA /path/to/cluster-ca.crt -CAkey /path/to/cluster-ca.key -CAcreateserial -out username.crt -days 365
   ```
2. **Create a kubeconfig for the user**:
   ```sh
   kubectl config set-credentials username \
     --client-certificate=username.crt \
     --client-key=username.key
   kubectl config set-context username-context \
     --cluster=<cluster-name> \
     --user=username
   kubectl config use-context username-context
   ```
   - Provide the generated config file to the user.

---

### **3. Set Up RBAC Permissions (Mandatory for Least Privilege)**
1. **Create a `Role` or `ClusterRole`** (define permissions):
   ```yaml
   # Example Role (namespace-scoped)
   apiVersion: rbac.authorization.k8s.io/v1
   kind: Role
   metadata:
     namespace: default
     name: pod-reader
   rules:
   - apiGroups: [""]
     resources: ["pods"]
     verbs: ["get", "list", "watch"]
   ```
   ```yaml
   # Example ClusterRole (cluster-scoped)
   apiVersion: rbac.authorization.k8s.io/v1
   kind: ClusterRole
   metadata:
     name: node-viewer
   rules:
   - apiGroups: [""]
     resources: ["nodes"]
     verbs: ["get", "list", "watch"]
   ```
2. **Bind the Role to the User**:
   ```yaml
   # RoleBinding (namespace-scoped)
   apiVersion: rbac.authorization.k8s.io/v1
   kind: RoleBinding
   metadata:
     name: read-pods
     namespace: default
   subjects:
   - kind: User
     name: "username"
     apiGroup: rbac.authorization.k8s.io
   roleRef:
     kind: Role
     name: pod-reader
     apiGroup: rbac.authorization.k8s.io
   ```
   ```yaml
   # ClusterRoleBinding (cluster-scoped)
   apiVersion: rbac.authorization.k8s.io/v1
   kind: ClusterRoleBinding
   metadata:
     name: view-nodes
   subjects:
   - kind: User
     name: "username"
     apiGroup: rbac.authorization.k8s.io
   roleRef:
     kind: ClusterRole
     name: node-viewer
     apiGroup: rbac.authorization.k8s.io
   ```

---

### **4. Distribute the kubeconfig Securely**
- Send the kubeconfig file via encrypted channels (e.g., **SSH**, **GPG**, or a secure file-sharing tool).
- Instruct the user to place it at `~/.kube/config` or use it with:
  ```sh
  kubectl --kubeconfig /path/to/user-config get pods
  ```

---

### **5. (Optional) Restrict Cluster Access Further**
- **Network Policies**: Limit access to the API server by IP.
- **Short-Lived Certificates**: Use tools like `cert-manager` to auto-expire credentials.
- **Audit Logging**: Monitor user activity with `--audit-policy-file`.

---

### **6. Verify Access**
Ask the user to run:
```sh
kubectl get pods
```
If permissions are correct, they’ll see only what they’re allowed to.

---

### **Alternative: Temporary Access with `kubectl proxy`**
If you don’t want to share credentials:
```sh
kubectl proxy --port=8080 &
```
Users can then access the cluster via `http://localhost:8080` on your machine (use SSH tunneling if remote).

---

### **Summary**
1. Choose an auth method (kubeconfig, tokens, OIDC).
2. Generate credentials and a kubeconfig.
3. Define RBAC roles/bindings.
4. Securely share the kubeconfig.
5. Restrict permissions to the least privilege.

For production, consider **OpenID Connect (OIDC)** or **SSO integration** (e.g., Dex, Keycloak) for centralized user management.