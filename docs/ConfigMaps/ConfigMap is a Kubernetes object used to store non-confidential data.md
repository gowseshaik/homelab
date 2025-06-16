## What is a ConfigMap?
A ConfigMap is a Kubernetes object used to store non-confidential data in key-value pairs. It allows you to decouple configuration artifacts from container images, making your applications more portable.

## Why use ConfigMaps?
- Separate configuration from application code
- Manage environment-specific configurations
- Update configurations without rebuilding images
- Share configurations between pods
- Maintain a single source of truth for configurations

## When to use ConfigMaps?
- Application configuration files
- Environment variables
- Command-line arguments
- Configuration data that doesn't contain sensitive information

## How to use ConfigMaps?

### Creating a ConfigMap
1. **Imperative command**:
   ```bash
   kubectl create configmap my-config --from-literal=key1=value1 --from-literal=key2=value2
   ```

2. **From a file**:
   ```bash
   kubectl create configmap my-config --from-file=path/to/config.file
   ```

3. **YAML definition**:
   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: game-config
   data:
     game.properties: |
       enemy.types=aliens,monsters
       player.maximum-lives=5
     ui.properties: |
       color.good=purple
       color.bad=yellow
   ```

### Using ConfigMaps in Pods
1. **As environment variables**:
   ```yaml
   env:
     - name: SPECIAL_LEVEL_KEY
       valueFrom:
         configMapKeyRef:
           name: special-config
           key: SPECIAL_LEVEL
   ```

2. **As volume mounts**:
   ```yaml
   volumes:
     - name: config-volume
       configMap:
         name: game-config
   containers:
     volumeMounts:
       - name: config-volume
         mountPath: /etc/config
   ```

### Updating ConfigMaps
```bash
kubectl edit configmap my-config
# or
kubectl create configmap my-config --from-literal=key=new-value --dry-run=client -o yaml | kubectl replace -f -
```

Note: Pods need to be restarted to pick up ConfigMap changes unless you're using a tool that watches for changes.

Here are the commands for working with the ConfigMap manifests and examples provided earlier:

### 1. Create ConfigMap from literal values
```bash
kubectl create configmap my-config \
  --from-literal=key1=value1 \
  --from-literal=key2=value2
```

### 2. Create ConfigMap from a file
```bash
# Create from a single file
kubectl create configmap game-config --from-file=game.properties

# Create from multiple files
kubectl create configmap game-config \
  --from-file=game.properties \
  --from-file=ui.properties
```

### 3. Create ConfigMap from YAML manifest
```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: game-config
data:
  game.properties: |
    enemy.types=aliens,monsters
    player.maximum-lives=5
  ui.properties: |
    color.good=purple
    color.bad=yellow
EOF
```

### 4. Create Pod using ConfigMap as environment variables
```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: configmap-env-pod
spec:
  containers:
    - name: test-container
      image: busybox
      command: ["/bin/sh", "-c", "env"]
      env:
        - name: SPECIAL_LEVEL_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: SPECIAL_LEVEL
  restartPolicy: Never
EOF
```

### 5. Create Pod using ConfigMap as volume
```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: configmap-volume-pod
spec:
  containers:
    - name: test-container
      image: busybox
      command: ["/bin/sh", "-c", "ls /etc/config && cat /etc/config/game.properties"]
      volumeMounts:
        - name: config-volume
          mountPath: /etc/config
  volumes:
    - name: config-volume
      configMap:
        name: game-config
  restartPolicy: Never
EOF
```

### 6. View ConfigMaps
```bash
# List all ConfigMaps
kubectl get configmaps

# View details of a specific ConfigMap
kubectl get configmap my-config -o yaml
kubectl describe configmap my-config
```

### 7. Update ConfigMap
```bash
# Edit directly
kubectl edit configmap my-config

# Replace entirely (using new values)
kubectl create configmap my-config \
  --from-literal=key1=new-value \
  --from-literal=key2=new-value2 \
  --dry-run=client -o yaml | kubectl replace -f -
```

### 8. Delete ConfigMap
```bash
kubectl delete configmap my-config
```

These commands cover all the scenarios mentioned in your original W3H explanation for ConfigMaps. You can run them in sequence to see how ConfigMaps work in Kubernetes.