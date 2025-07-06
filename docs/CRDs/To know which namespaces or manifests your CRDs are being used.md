<span style="color:#4caf50;"><b>Created:</b> 2025-07-06</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
### 🔍 Step 1: List all resources of a CRD kind

If your CRD is named `sealedsecrets.bitnami.com`, then the resource kind is `SealedSecret`.

Run:

```bash
kubectl get sealedsecrets --all-namespaces
```

This shows all instances (usages) of `SealedSecret` in your cluster across all namespaces.

Replace `sealedsecrets` with the plural resource name of your CRD.

To find the kind and plural name from CRD:

```bash
kubectl get crd sealedsecrets.bitnami.com -o yaml | grep kind
# kind: SealedSecret
```

### 🔍 Step 2: Search for CRD usage in YAML manifests (GitOps or local repo)

If you use Git for infra (e.g., ArgoCD), run:

```bash
grep -R "kind: SealedSecret" .
```

This shows all YAML files that define `SealedSecret` objects.

### 🔍 Step 3: Get full YAML of existing CRD objects

To see how it's used (what fields, metadata, etc.):

```bash
kubectl get sealedsecrets -n default -o yaml
```

Replace `sealedsecrets` and `default` with your CRD and namespace.

### 🧠 Summary

|Task|Command Example|
|---|---|
|List instances of a CRD|`kubectl get <crd-resource> --all-namespaces`|
|Check CRD usage in Git/YAML files|`grep -R "kind: <CRDKind>" .`|
|View full object definition|`kubectl get <crd-resource> -o yaml`|
