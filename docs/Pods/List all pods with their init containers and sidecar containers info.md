```bash
# List all pods with their init containers and sidecar containers info

kubectl get pods --all-namespaces -o json | jq -r '
  .items[] | 
  {
    namespace: .metadata.namespace,
    pod: .metadata.name,
    initContainers: (.spec.initContainers // [] | map(.name)),
    containers: (.spec.containers // [] | map(.name))
  } | 
  "Namespace: \(.namespace)\nPod: \(.pod)\nInit Containers: \(.initContainers | join(", "))\nContainers: \(.containers | join(", "))\n"
'
```

If you don't have `jq`, you can do a simpler approach:

```bash
kubectl get pods --all-namespaces -o custom-columns=NAMESPACE:.metadata.namespace,POD:.metadata.name,INIT_CONTAINERS:.spec.initContainers[*].name,CONTAINERS:.spec.containers[*].name
```

This shows init containers and sidecar (all containers except main) by pod. Sidecars are normally just additional containers listed alongside main containers.