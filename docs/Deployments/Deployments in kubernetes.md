# Deployments in Kubernetes: A Comprehensive Guide

## What are Deployments?

Deployments are Kubernetes objects that provide declarative updates for Pods and ReplicaSets. They allow you to describe an application's life cycle, including which images to use, the number of pods, and how to update them.

## Why Use Deployments?

1. **Rolling updates**: Update applications with zero downtime
2. **Rollback capability**: Revert to previous versions if something goes wrong
3. **Scaling**: Easily scale your application up or down
4. **Self-healing**: Automatically replaces failed pods
5. **Version tracking**: Maintain deployment history

## When to Use Deployments?

- When you need to run multiple replicas of your application
- When you need rolling updates and rollbacks
- For stateless applications (for stateful apps, consider StatefulSets)
- When you need declarative management of pods

## How to Use Deployments

### Basic Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

## Types of Deployment Strategies

1. **Rolling Update (default)**
   - Gradually replaces old pods with new ones
   - No downtime during update
   - Controlled by `maxUnavailable` and `maxSurge` parameters

2. **Recreate**
   - Kills all old pods before creating new ones
   - Results in downtime
   - Useful when your application can't run multiple versions simultaneously

## Deployment Commands Cheatsheet

### Basic Commands
```bash
# Create a deployment
kubectl create deployment nginx --image=nginx

# Get deployments
kubectl get deployments

# Describe a deployment
kubectl describe deployment <deployment-name>

# Delete a deployment
kubectl delete deployment <deployment-name>
```

### Scaling
```bash
# Scale a deployment
kubectl scale deployment <deployment-name> --replicas=5

# Auto-scale a deployment
kubectl autoscale deployment <deployment-name> --min=2 --max=5 --cpu-percent=80
```

### Updates and Rollbacks
```bash
# Update deployment image
kubectl set image deployment/<deployment-name> nginx=nginx:1.16.1

# Check rollout status
kubectl rollout status deployment/<deployment-name>

# Pause a rollout
kubectl rollout pause deployment/<deployment-name>

# Resume a rollout
kubectl rollout resume deployment/<deployment-name>

# Rollback to previous version
kubectl rollout undo deployment/<deployment-name>

# Rollback to specific revision
kubectl rollout undo deployment/<deployment-name> --to-revision=2

# View rollout history
kubectl rollout history deployment/<deployment-name>
```

### Advanced Operations
```bash
# Dry-run to test deployment changes
kubectl apply -f deployment.yaml --dry-run=client

# View deployment as YAML
kubectl get deployment <deployment-name> -o yaml

# View deployment as JSON
kubectl get deployment <deployment-name> -o json

# Edit deployment
kubectl edit deployment <deployment-name>
```

### Troubleshooting
```bash
# View deployment events
kubectl describe deployment <deployment-name> | grep -i events -A10

# View associated pods
kubectl get pods -l app=<label-selector>

# View pod logs
kubectl logs <pod-name>
```

Remember that deployments work hand-in-hand with other Kubernetes objects like Services to expose your application to the network.