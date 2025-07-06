<span style="color:#4caf50;"><b>Created:</b> 2025-07-06</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

Yes, you can list all controllers running in your Kubernetes cluster by checking the pods in the `kube-system` namespace and other namespaces where controllers commonly run.
```bash
# List all pods in kube-system (common place for core controllers)
kubectl get pods -n kube-system

# List pods in all namespaces (to find controllers elsewhere)
kubectl get pods --all-namespaces

# Filter pods by name pattern (e.g., controller)
kubectl get pods --all-namespaces | grep controller
```

If you want to see specifically which controllers are installed as CustomResourceDefinitions (CRDs) or operators:
```bash
# List all CRDs (often installed by controllers/operators)
kubectl get crds

# Check deployed operators via deployments
kubectl get deployments --all-namespaces | grep operator
```

For Sealed Secrets controller, for example:
```bash
kubectl get pods -n kube-system -l name=sealed-secrets-controller
```

This will tell you if the sealed-secrets controller is running.

**CRDs (CustomResourceDefinitions)** are **custom resource types** you can add to Kubernetes to extend its API.

- When you install a CRD, you define a new kind of object your cluster understands.
- To **make those CRDs useful**, you usually run a **controller** (often called an operator) that watches and manages those custom resources.

So:

|Term|Meaning|
|---|---|
|Controller|The logic/process that manages resources and enforces desired state (built-in or custom)|
|CRD|Custom resource type you add to Kubernetes|

Controllers often come bundled with CRDs (like in Operators), but **a controller is not the same as a CRD**.

Example:

- Sealed Secrets has a CRD `SealedSecret` and a controller that watches SealedSecret objects and creates Secrets.
- The CRD is just the schema.
- The controller does the work.
