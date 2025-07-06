<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
## What are Tolerations?

Tolerations are Kubernetes mechanisms that allow pods to be scheduled onto nodes with matching taints. They work in conjunction with taints to enable advanced scheduling scenarios where certain nodes are "reserved" for specific workloads.

## Why Use Tolerations?

Tolerations are used when you need to:
- Schedule pods on specialized nodes (like GPU nodes)
- Allow critical workloads to run on reserved nodes
- Handle node maintenance gracefully
- Implement multi-tenant clusters with dedicated resources

## When to Use Tolerations?

Common use cases:
- Nodes with specialized hardware
- Nodes reserved for specific teams/applications
- Nodes that might be problematic for some workloads (e.g., spot instances)
- Nodes undergoing maintenance

## How to Use Tolerations?

### Basic Example: GPU Workload

1. **Taint the GPU node**:
```bash
kubectl taint nodes gpu-node-1 hardware=gpu:NoSchedule
```

2. **Create a pod with matching toleration**:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod
spec:
  containers:
  - name: cuda-container
    image: nvidia/cuda:11.0-base
    resources:
      limits:
        nvidia.com/gpu: 1
  tolerations:
  - key: "hardware"
    operator: "Equal"
    value: "gpu"
    effect: "NoSchedule"
```

### Advanced Example: Spot Instance with PreferNoSchedule

1. **Taint the spot instance nodes**:
```bash
kubectl taint nodes spot-node-1 instance-type=spot:PreferNoSchedule
```

2. **Pod with toleration and node selector**:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: cost-optimized-app
spec:
  containers:
  - name: app
    image: my-app:latest
  tolerations:
  - key: "instance-type"
    operator: "Equal"
    value: "spot"
    effect: "PreferNoSchedule"
  nodeSelector:
    instance-type: spot
```

### Maintenance Example: Allow pod during node drain

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: critical-app
spec:
  containers:
  - name: app
    image: critical-app:latest
  tolerations:
  - key: "node.kubernetes.io/unschedulable"
    operator: "Exists"
    effect: "NoSchedule"
  - key: "node.kubernetes.io/unreachable"
    operator: "Exists"
    effect: "NoExecute"
    tolerationSeconds: 6000  # Keep running for 100 minutes if node becomes unreachable
```

## Key Points to Remember

1. Tolerations don't guarantee pod scheduling - they just allow it if other conditions are met
2. Use `operator: "Exists"` when you don't care about the value
3. `tolerationSeconds` controls how long a pod stays bound to an unreachable node
4. Combine tolerations with nodeSelectors/affinity for precise scheduling

Tolerations are powerful tools for advanced scheduling scenarios in Kubernetes, especially when working with heterogeneous node pools or specialized hardware.