To discover **Kubernetes API resources** and their available **fields/values** for YAML files, you can use the following commands:

---

### **1. List All API Resources**
```sh
kubectl api-resources
```
**Output Example:**
```
NAME          SHORTNAMES   APIVERSION     NAMESPACED   KIND
pods          po           v1             true         Pod
deployments   deploy       apps/v1        true         Deployment
services      svc          v1             true         Service
ingresses     ing          networking.k8s.io/v1   true  Ingress
clusterissuers             cert-manager.io/v1     false   ClusterIssuer
```

The `false` value means that `ClusterIssuer` is a cluster-scoped resource, not a namespaced resource. Here's what this means:

1. **`false` (cluster-scoped)**:
    - The resource exists at the cluster level
    - Not tied to any specific namespace
    - Can be referenced from any namespace
    - Typically includes resources that affect the entire cluster
        
2. **`true` (namespaced)**
    - The resource exists within a specific namespace
    - Must be created in a namespace
    - Only accessible within that namespace

### **2. Get API Version for a Resource**
```sh
kubectl explain <resource> | head -n 2
```
**Example:**
```sh
kubectl explain deployment | head -n 2
```
**Output:**
```
KIND:     Deployment
VERSION:  apps/v1
```

---

### **3. View All Available Fields in a Resource**
```sh
kubectl explain <resource> --recursive
```
**Example (Deployment):**
```sh
kubectl explain deployment --recursive
```
**Output (Partial):**
```yaml
KIND:     Deployment
VERSION:  apps/v1
DESCRIPTION:
     Deployment enables declarative updates for Pods and ReplicaSets.
FIELDS:
   apiVersion   <string>
   kind <string>
   metadata     <Object>
      annotations       <map[string]string>
      creationTimestamp <string>
      name      <string>
      namespace <string>
   spec <Object>
      replicas  <integer>
      selector  <Object>
         matchLabels    <map[string]string>
      template  <Object>
         metadata       <Object>
            labels      <map[string]string>
         spec   <Object>
            containers  <[]Object>
               name     <string>
               image    <string>
               ports    <[]Object>
                  containerPort    <integer>
...
```

---

### **4. Check Specific Field Details**
```sh
kubectl explain <resource>.<field>
```
**Examples:**
```sh
# Check Deployment's `spec.strategy`
kubectl explain deployment.spec.strategy

# Check Pod's `spec.containers`
kubectl explain pod.spec.containers

# Check Ingress `spec.rules`
kubectl explain ingress.spec.rules
```

---

### **5. List All Possible Values for Enums (e.g., `restartPolicy`)**
```sh
kubectl explain pod.spec.restartPolicy
```
**Output:**
```
KIND:     Pod
VERSION:  v1
FIELD:    restartPolicy <string>
DESCRIPTION:
     Restart policy for all containers within the pod.
     Possible enum values:
     - `"Always"`
     - `"OnFailure"`
     - `"Never"`
```

---

### **6. View OpenAPI/Swagger Docs (Full Schema)**
```sh
kubectl get --raw /openapi/v2 | jq . | less
```
(Use `jq` for filtering, e.g., `kubectl get --raw /openapi/v2 | jq '.definitions["io.k8s.api.apps.v1.Deployment"]'`)

---

### **7. Check CRD (Custom Resource) Schema**
```sh
kubectl get crd <crd-name> -o yaml
```
**Example:**
```sh
kubectl get crd traefikservices.traefik.io -o yaml
```

---

### **8. Shortcut for Common Resources**
| Resource  | Command to View Schema |
|-----------|------------------------|
| Pod       | `kubectl explain pod` |
| Deployment | `kubectl explain deployment` |
| Service   | `kubectl explain service` |
| Ingress   | `kubectl explain ingress` |
| ConfigMap | `kubectl explain configmap` |
| Secret    | `kubectl explain secret` |

---

### **Summary Cheatsheet**
| Command | Purpose |
|---------|---------|
| `kubectl api-resources` | List all available resources |
| `kubectl explain <resource>` | Show YAML structure of a resource |
| `kubectl explain <resource> --recursive` | Show all nested fields |
| `kubectl explain <resource>.<field>` | Check a specific field |
| `kubectl get --raw /openapi/v2` | View full OpenAPI schema |

These commands help you **discover valid fields and values** when writing Kubernetes YAML files. 🚀