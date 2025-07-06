<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

Configuring **Keycloak** for Kubernetes authentication allows centralized user management via **OIDC (OpenID Connect)**. Below are the step-by-step instructions to set this up:

---

## **Step 1: Set Up Keycloak**
### **1.1 Install & Configure Keycloak**
- Deploy Keycloak (standalone or in Kubernetes):
  ```sh
  helm repo add bitnami https://charts.bitnami.com/bitnami
  helm install keycloak bitnami/keycloak \
    --set auth.adminUser=admin \
    --set auth.adminPassword=admin \
    --set service.type=LoadBalancer
  ```
- Access the Keycloak admin console (`http://<keycloak-ip>:8080/admin`).

### **1.2 Create a New Realm**
- Go to **Admin Console** → **Add Realm** (e.g., `kubernetes`).

### **1.3 Create a Client for Kubernetes**
- Navigate to **Clients** → **Create**:
  - **Client ID**: `kubernetes`
  - **Client Protocol**: `openid-connect`
  - **Root URL**: `https://<k8s-api-server>`
- Under **Settings**:
  - **Access Type**: `confidential`
  - **Valid Redirect URIs**: `*` (or restrict to allowed domains)
  - **Save**.

### **1.4 Create Users & Groups**
- Go to **Users** → **Add User** (e.g., `dev-user`).
- Set a password under **Credentials**.
- (Optional) Assign users to groups (e.g., `dev-team`, `admin-team`).

### **1.5 Configure Mappers (for Group/Role Claims)**
- Under **Clients** → `kubernetes` → **Mappers** → **Create**:
  - **Name**: `groups`
  - **Mapper Type**: `Group Membership`
  - **Token Claim Name**: `groups`
  - **Full group path**: `OFF`
  - **Add to ID token**: `ON`
  - **Add to access token**: `ON`

---

## **Step 2: Configure Kubernetes API Server for OIDC**
### **2.1 Modify API Server Flags**
Edit `/etc/kubernetes/manifests/kube-apiserver.yaml` (on the control plane) and add:
```yaml
spec:
  containers:
  - command:
    - kube-apiserver
    - --oidc-issuer-url=https://<keycloak-url>/realms/kubernetes
    - --oidc-client-id=kubernetes
    - --oidc-username-claim=preferred_username
    - --oidc-groups-claim=groups
    - --oidc-ca-file=/etc/ssl/certs/keycloak-ca.crt  # If Keycloak uses HTTPS (recommended)
```
- Restart the API server (if not auto-applied):
  ```sh
  systemctl restart kubelet
  ```

### **2.2 (Optional) Add Keycloak CA to Kubernetes Trust Store**
If Keycloak uses HTTPS (self-signed cert):
```sh
openssl s_client -connect <keycloak-url>:443 -showcerts </dev/null 2>/dev/null | openssl x509 -outform PEM > keycloak-ca.crt
sudo cp keycloak-ca.crt /etc/ssl/certs/
sudo update-ca-certificates
```

---

## **Step 3: Configure kubectl for Keycloak Auth**
### **3.1 Install `kubelogin` (OIDC Helper)**
```sh
wget https://github.com/int128/kubelogin/releases/download/v1.28.0/kubelogin_linux_amd64.zip
unzip kubelogin_linux_amd64.zip
sudo mv kubelogin /usr/local/bin/
```

### **3.2 Create a kubeconfig for OIDC**
```sh
kubectl config set-credentials dev-user \
  --auth-provider=oidc \
  --auth-provider-arg=idp-issuer-url=https://<keycloak-url>/realms/kubernetes \
  --auth-provider-arg=client-id=kubernetes \
  --auth-provider-arg=client-secret=<keycloak-client-secret> \
  --auth-provider-arg=refresh-token=<optional> \
  --auth-provider-arg=idp-certificate-authority=/etc/ssl/certs/keycloak-ca.crt
```
- Get the `client-secret` from Keycloak (**Clients** → `kubernetes` → **Credentials**).

### **3.3 Test Authentication**
```sh
kubectl get pods
```
- A browser window will open for Keycloak login.

---

## **Step 4: Set Up RBAC for Keycloak Users**
### **4.1 Create ClusterRoleBinding (Example)**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: keycloak-admin-binding
subjects:
- kind: User
  name: "admin@example.com"  # Must match OIDC username_claim
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
```

### **4.2 (Optional) Map Groups to Roles**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-team-binding
  namespace: default
subjects:
- kind: Group
  name: "dev-team"  # From Keycloak groups
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: edit
  apiGroup: rbac.authorization.k8s.io
```

---

## **Step 5: Secure Keycloak (Optional)**
- Enable **MFA** in Keycloak.
- Set **Token Lifetimes** (e.g., 15-minute access tokens).
- Use **Network Policies** to restrict API server access.

---

## **Troubleshooting**
| **Issue**                          | **Solution** |
|------------------------------------|-------------|
| `OIDC: invalid bearer token`       | Check `--oidc-issuer-url` matches Keycloak realm. |
| `x509: certificate signed by unknown authority` | Add Keycloak CA to trust store. |
| No groups in token                 | Ensure `groups` mapper is configured in Keycloak. |

---

### **Final Notes**
✅ **Keycloak + OIDC** is ideal for enterprise Kubernetes access.  
✅ **RBAC** ensures least privilege.  
✅ **Short-lived tokens** improve security.  

Would you like help automating this with **Terraform** or **ArgoCD**?