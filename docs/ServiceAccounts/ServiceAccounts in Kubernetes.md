## What are ServiceAccounts in Kubernetes?

ServiceAccounts are Kubernetes objects that provide an identity for processes running in Pods. They:
- Are namespaced resources (exist within a specific namespace)
- Are used to authenticate Pods with the Kubernetes API server
- Are automatically mounted into Pods at `/var/run/secrets/kubernetes.io/serviceaccount`
- Are different from UserAccounts which are for human users

## Why use ServiceAccounts?

ServiceAccounts are essential because:
1. **Security**: They enable least-privilege access control for Pods
2. **Authentication**: They allow Kubernetes to identify which Pod is making API requests
3. **Authorization**: They work with RBAC (Role-Based Access Control) to define what actions Pods can perform
4. **Automation**: They enable secure communication between Pods and the API server without manual credential management

## When to use ServiceAccounts?

You should use ServiceAccounts when:
- A Pod needs to interact with the Kubernetes API
- Different Pods need different levels of access to cluster resources
- You need to restrict what certain workloads can do in your cluster
- You're implementing CI/CD pipelines that interact with Kubernetes
- You're running custom controllers or operators

## How to use ServiceAccounts?

### Basic Usage
1. **Default ServiceAccount**: Every namespace has a default ServiceAccount automatically used by Pods
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: mypod
   spec:
     containers:
     - name: mycontainer
       image: myimage
     # Automatically uses the 'default' ServiceAccount
   ```

2. **Creating a custom ServiceAccount**
   ```bash
   kubectl create serviceaccount my-sa
   ```

3. **Assigning to a Pod**
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: mypod
   spec:
     serviceAccountName: my-sa  # custom ServiceAccount
     containers:
     - name: mycontainer
       image: myimage
   ```

### Advanced Usage
1. **Creating RBAC bindings** (ClusterRole and RoleBinding)
   ```yaml
   apiVersion: rbac.authorization.k8s.io/v1
   kind: Role
   metadata:
     namespace: default
     name: pod-reader
   rules:
   - apiGroups: [""]
     resources: ["pods"]
     verbs: ["get", "watch", "list"]
   
   apiVersion: rbac.authorization.k8s.io/v1
   kind: RoleBinding
   metadata:
     name: read-pods
     namespace: default
   subjects:
   - kind: ServiceAccount
     name: my-sa
     namespace: default
   roleRef:
     kind: Role
     name: pod-reader
     apiGroup: rbac.authorization.k8s.io
   ```

2. **Using in Deployments**
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: my-deployment
   spec:
     replicas: 3
     template:
       spec:
         serviceAccountName: my-sa
         containers:
         - name: mycontainer
           image: myimage
   ```

3. **Inspecting the token** (from inside a Pod)
   ```bash
   # Inside a Pod:
   cat /var/run/secrets/kubernetes.io/serviceaccount/token
   ```

### Best Practices
1. Avoid using the default ServiceAccount for production workloads
2. Create dedicated ServiceAccounts for different types of workloads
3. Follow the principle of least privilege when assigning permissions
4. Regularly audit ServiceAccount permissions
5. Consider using `automountServiceAccountToken: false` for Pods that don't need API access

### Troubleshooting
- If a Pod can't access the API, check:
  - Does the ServiceAccount exist?
  - Are the RBAC permissions correct?
  - Is the token properly mounted?
  - Use `kubectl auth can-i` commands to verify permissions