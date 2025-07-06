<span style="color:#4caf50;"><b>Created:</b> 2025-07-01</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

Kubernetes RBAC(Role-Based Access Control) like you're explaining it to your junior.

### 🧠 **Imagine This Simple Setup**

You are the **admin** of an office building (Kubernetes cluster).  
There are:

- **People** (users or service accounts)
- **Rooms** (resources like pods, configmaps, etc.)
- **Keys** (permissions)

You decide:

- Who can **enter which room**
- What they can **do inside**

### 🗝️ **RBAC = Giving Right Keys to Right People**

RBAC uses 4 main objects:

|Object|Meaning|Example|
|---|---|---|
|**Role**|Defines "what someone can do" in one namespace|"Can read pods in `dev`"|
|**ClusterRole**|Same as Role, but works across all namespaces|"Can delete pods everywhere"|
|**RoleBinding**|Gives a Role to a person in a namespace|"Give read-pods Role to dev-user"|
|**ClusterRoleBinding**|Like RoleBinding but across all namespaces|"Give admin Role to ops-team globally"|

---

### 🪪 **Simple RBAC Example**

You want to **allow dev-user to read pods in `demo` namespace only**.

#### 🔹 Step 1: Create the **Role**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: read-pods
  namespace: demo
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
```

🔍 This says: “Whoever gets this Role can `get` and `list` pods in namespace `demo`.”

#### 🔹 Step 2: Bind the Role to a User

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: bind-read-pods
  namespace: demo
subjects:
- kind: User
  name: dev-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: read-pods
  apiGroup: rbac.authorization.k8s.io
```

🔍 This means: "Give `read-pods` Role to `dev-user` in the `demo` namespace."

### 👨‍🏫 **Final Summary**

|Thing|Real-World Analogy|
|---|---|
|**Role**|Job description: “Can read rooms A and B”|
|**RoleBinding**|Giving that job to a person|
|**User** or **ServiceAccount**|The employee (or robot) doing the job|
### 🧪 Test It

```bash
kubectl auth can-i list pods --namespace=demo --as=dev-user
```

Let me know if you want examples for:

- writing permissions
- admin role
- service account RBAC

Perfect — here’s a simple **set of examples** with **RBAC permissions** that cover:

1. ✅ Read-only access (basic user)
2. ✍️ Read + Write access (developer)
3. 🛠️ Full access (admin)
4. 🤖 Service Account-based access (for CI/CD pods)

### ✅ 1. **Read-Only Access (User)**

#### Role (read-only for pods)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: demo
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
```

#### RoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-reader-binding
  namespace: demo
subjects:
- kind: User
  name: dev-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### ✍️ 2. **Read + Write Access (Developer)**

#### Role (manage pods, deployments)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: dev-role
  namespace: demo
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "create", "delete"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "create", "delete"]
```

#### RoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-role-binding
  namespace: demo
subjects:
- kind: User
  name: dev-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: dev-role
  apiGroup: rbac.authorization.k8s.io
```

### 🛠️ 3. **Admin Access (Full rights in all namespaces)**

#### ClusterRoleBinding (use built-in `cluster-admin` role)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: give-admin-to-user
subjects:
- kind: User
  name: admin-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
```

### 🤖 4. **Service Account-Based Access (for pods, CI/CD)**

#### Role (read secrets)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: demo
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list"]
```

#### RoleBinding to ServiceAccount

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: bind-secret-reader
  namespace: demo
subjects:
- kind: ServiceAccount
  name: ci-job
  namespace: demo
roleRef:
  kind: Role
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

### ✅ Apply All:

```bash
kubectl apply -f role.yaml
kubectl apply -f rolebinding.yaml
```

- If you want all of them zipped into one YAML
- If your users are authenticated via OIDC/LDAP or using service accounts only

Great question — here's a clear and simple explanation of **authentication methods in Kubernetes**, focusing on:

- ✅ Service Account (default in pods)
- 🔐 OIDC (e.g. Keycloak, Azure AD, Google)
- 👥 LDAP (via Dex, Keycloak, etc.)

## ✅ 1. **Service Account Authentication** (default in pods)

- Every pod gets a service account by default.
- Kubernetes uses **JWT tokens** from `/var/run/secrets/kubernetes.io/serviceaccount/token`
- Used for automated tools (CI/CD, controllers, etc.)

### How to use:

1. Create a service account:

```bash
kubectl create serviceaccount sa-ci --namespace demo
```

2. Bind roles to it (RBAC):

```yaml
kind: RoleBinding
...
subjects:
- kind: ServiceAccount
  name: sa-ci
  namespace: demo
```

3. In a pod/deployment:

```yaml
serviceAccountName: sa-ci
```

✅ Used internally, no login needed manually.

## 🔐 2. **OIDC Authentication** (Users login via Google, Azure AD, Keycloak, etc.)

### Flow:

1. You connect your Kubernetes API server to an OIDC identity provider.
2. The user logs in via `kubectl` using `oidc` tokens.
3. You create RBAC bindings based on their **OIDC username or groups**.

### API Server Flags Example:

```bash
--oidc-issuer-url=https://accounts.google.com
--oidc-client-id=k8s-auth
--oidc-username-claim=email
--oidc-groups-claim=groups
```

Then bind roles like:

```yaml
subjects:
- kind: User
  name: gowse@example.com
```

✅ Best for teams and real-user access.

## 👥 3. **LDAP Authentication** (via Dex or Keycloak)

Kubernetes **does not natively support LDAP**, so you use an **identity proxy**:

|Tool|Purpose|
|---|---|
|**Dex**|Lightweight OIDC provider that connects to LDAP|
|**Keycloak**|Identity provider that supports OIDC + LDAP|
|**Pinniped**|Modern OIDC provider with LDAP support|
|**Auth0**|Cloud-based solution that supports LDAP backend|

### Example Flow:

1. Set up **Dex** or **Keycloak** to connect to your LDAP
2. Kubernetes API uses OIDC flags to integrate with them (same as above)
3. You assign RBAC based on LDAP users/groups (via OIDC claims)

## ✅ Summary Table

|Method|For|Needs OIDC?|Needs RBAC?|Login Type|
|---|---|---|---|---|
|**ServiceAccount**|Pods, automation|❌|✅|Auto-attached in pods|
|**OIDC**|Real users|✅|✅|`kubectl` login with token|
|**LDAP**|Real users (via OIDC proxy)|✅ (via Dex/Keycloak)|✅|LDAP login via OIDC token|
Let me know if:

- You want a full OIDC setup with Google/Keycloak
- You want a working Dex+LDAP example
- You want to generate tokens manually for testing