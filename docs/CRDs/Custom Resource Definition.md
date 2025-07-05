- Sealed Secrets has a CRD `SealedSecret` and a controller that watches SealedSecret objects and creates Secrets.
- The CRD is just the schema.
- The controller does the work.
Note: Controllers often come bundled with CRDs (like in Operators), but **a controller is not the same as a CRD**.
### **1. What are CRDs?**  
**Definition:**  
CRDs (**Custom Resource Definitions**) extend the Kubernetes API to allow users to create and manage **custom resources** (besides built-in resources like Pods, Deployments, etc.).  

**Key Concepts:**  
- **Custom Resource (CR):** An instance of a CRD (e.g., `MySQLDatabase`, `RedisCluster`).  
- **CRD:** The schema/definition that describes the custom resource (like a blueprint).  

**Example:**  
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: mysqlsamples.example.com
spec:
  group: example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema: {...}
  scope: Namespaced
  names:
    plural: mysqlsamples
    singular: mysqlsample
    kind: MySQLSample
```

---

### **2. Why Use CRDs?**  
**Purpose/Benefits:**  
- **Extend Kubernetes:** Add domain-specific resources (e.g., `PostgresDB`, `TensorFlowJob`).  
- **Declarative APIs:** Manage applications/resources using `kubectl` like native objects.  
- **Automation:** Integrate with operators (e.g., `etcd-operator`) for lifecycle management.  
- **Reusability:** Share CRDs across teams/organizations.  

**Use Cases:**  
- Databases, ML workloads, CI/CD pipelines, etc.  

---

### **3. When to Use CRDs?**  
**Scenarios:**  
- When Kubernetes lacks a built-in resource for your use case.  
- When you need a **declarative API** for your application.  
- When paired with a **Kubernetes Operator** for complex logic (e.g., backup, scaling).  

**Alternatives:**  
- Use **ConfigMaps/Secrets** for simple configurations.  
- Use **Helm charts** for packaging (but Helm doesn’t provide API extensions).  

---

### **4. How to Use CRDs?**  
**Steps to Create/Use a CRD:**  

#### **1. Define the CRD**  
```yaml
# mysql-crd.yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: mysqlsamples.example.com
spec:
  group: example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                dbName:
                  type: string
                replicas:
                  type: integer
  scope: Namespaced
  names:
    plural: mysqlsamples
    singular: mysqlsample
    kind: MySQLSample
```
Apply it:  
```sh
kubectl apply -f mysql-crd.yaml
```

#### **2. Create a Custom Resource (CR)**  
```yaml
# mysql-instance.yaml
apiVersion: example.com/v1
kind: MySQLSample
metadata:
  name: my-mysql
spec:
  dbName: "mydb"
  replicas: 2
```
Apply it:  
```sh
kubectl apply -f mysql-instance.yaml
```

#### **3. Verify**  
```sh
kubectl get crd                          # List CRDs
kubectl get mysqlsamples                 # List custom resources
kubectl describe mysqlsamples my-mysql   # Inspect a CR
```

#### **4. (Optional) Build an Operator**  
Use tools like:  
- **Kubebuilder**  
- **Operator SDK**  
to automate CRD management (e.g., reconcile loops).

---

### **Summary (W3H Table)**  
| **Aspect** | **Description** |
|------------|----------------|
| **What**   | Kubernetes API extension for custom resources. |
| **Why**    | To add domain-specific resources declaratively. |
| **When**   | When built-in resources are insufficient. |
| **How**    | Define CRD → Create CR → (Optional) Use Operator. |

