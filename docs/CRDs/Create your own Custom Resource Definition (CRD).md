
<span style="color:#4caf50;"><b>Created:</b> 2025-07-06</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
### ✅ What You Need to Do
When you're extending Kubernetes with **your own custom types** — without touching the core Kubernetes code — you use:
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
```

|Goal|Use|
|---|---|
|Use core Kubernetes objects|`apiVersion: v1`, `apps/v1`, etc.|
|Define your own custom resource type|`apiVersion: apiextensions.k8s.io/v1`|
|Interact with your new object type|`apiVersion: yourdomain.com/v1`, etc.|

✅ So yes — **all CRD definitions must use `apiextensions.k8s.io/v1`** to register a new type into the Kubernetes API server.


### 🛠️ Step 1: Define the CRD (structure and schema)

**crd.yaml**

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: hellos.example.com    # plural.name.group
spec:
  group: example.com
  names:
    kind: Hello               # Singular kind
    plural: hellos
    singular: hello
    shortNames:
    - hi
  scope: Namespaced
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
              message:
                type: string
```

Apply it:

```bash
kubectl apply -f crd.yaml
```

---

### 🛠️ Step 2: Create a custom resource using your CRD

**hello.yaml**

```yaml
apiVersion: example.com/v1
kind: Hello
metadata:
  name: greeting
spec:
  message: "Hello, CRD World!"
```

Apply it:

```bash
kubectl apply -f hello.yaml
```

---

### 🛠️ Step 3: (Optional) Build a controller to act on your CRD

Without a controller, CRDs are just data. To make them **do something**, write a controller in Go, Python, or use tools like:

- **kubebuilder** (Go-based)
- **operator-sdk**
- **kopf** (Python)
- **Metacontroller**
- **Pulumi/Helm** (for lightweight logic)

---

### 🔍 Step 4: See your CRD in action

```bash
kubectl get hellos
kubectl describe hello greeting
```
