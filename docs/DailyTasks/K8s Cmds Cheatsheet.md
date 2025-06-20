## Cluster Management
- `kubectl cluster-info` - Display cluster information
- `kubectl get nodes` - List all nodes in the cluster
- `kubectl describe node <node-name>` - Show detailed information about a specific node
- `kubectl top node` - Show resource usage (CPU/Memory) for nodes
- `kubectl top pod` - Show resource usage for pods
- `kubectl cordon <node-name>` - Mark node as unschedulable
- `kubectl uncordon <node-name>` - Mark node as schedulable
- `kubectl drain <node-name>` - Drain node in preparation for maintenance

## Namespace Operations
- `kubectl get namespaces` - List all namespaces
- `kubectl create namespace <namespace-name>` - Create a new namespace
- `kubectl config set-context --current --namespace=<namespace-name>` - Set default namespace for current context
- `kubectl delete namespace <namespace-name>` - Delete a namespace

## Pod Operations
- `kubectl get pods` - List all pods in current namespace
- `kubectl get pods -A` - List all pods in all namespaces
- `kubectl get pods -o wide` - List pods with additional details (IP, node)
- `kubectl describe pod <pod-name>` - Show detailed information about a pod
- `kubectl logs <pod-name>` - Print pod logs
- `kubectl logs -f <pod-name>` - Stream pod logs (follow)
- `kubectl logs <pod-name> -c <container-name>` - Print logs from a specific container in a pod
- `kubectl exec -it <pod-name> -- /bin/bash` - Execute a command in a pod (interactive)
- `kubectl delete pod <pod-name>` - Delete a pod
- `kubectl port-forward <pod-name> <local-port>:<pod-port>` - Forward a local port to a pod

## Deployment Operations
- `kubectl get deployments` - List all deployments
- `kubectl describe deployment <deployment-name>` - Show deployment details
- `kubectl create deployment <name> --image=<image>` - Create a deployment
- `kubectl scale deployment <deployment-name> --replicas=<number>` - Scale a deployment
- `kubectl rollout status deployment/<deployment-name>` - Check rollout status
- `kubectl rollout history deployment/<deployment-name>` - View rollout history
- `kubectl rollout undo deployment/<deployment-name>` - Rollback to previous version
- `kubectl rollout undo deployment/<deployment-name> --to-revision=<number>` - Rollback to specific revision
- `kubectl set image deployment/<deployment-name> <container-name>=<new-image>` - Update deployment image

## Service Operations
- `kubectl get services` - List all services
- `kubectl describe service <service-name>` - Show service details
- `kubectl expose deployment <deployment-name> --port=<port> --target-port=<target-port> --type=<type>` - Expose a deployment as a service
- `kubectl delete service <service-name>` - Delete a service

## ConfigMap & Secrets
- `kubectl get configmaps` - List all configmaps
- `kubectl create configmap <name> --from-file=<path-to-file>` - Create configmap from file
- `kubectl create configmap <name> --from-literal=<key>=<value>` - Create configmap from literal
- `kubectl get secrets` - List all secrets
- `kubectl create secret generic <name> --from-literal=<key>=<value>` - Create secret from literal
- `kubectl create secret generic <name> --from-file=<path-to-file>` - Create secret from file

## StatefulSets & DaemonSets
- `kubectl get statefulsets` - List all statefulsets
- `kubectl get daemonsets` - List all daemonsets

## Jobs & CronJobs
- `kubectl get jobs` - List all jobs
- `kubectl get cronjobs` - List all cronjobs

## Persistent Volumes & Claims
- `kubectl get pv` - List persistent volumes
- `kubectl get pvc` - List persistent volume claims

## RBAC & Security
- `kubectl get roles` - List roles
- `kubectl get rolebindings` - List role bindings
- `kubectl get clusterroles` - List cluster roles
- `kubectl get clusterrolebindings` - List cluster role bindings
- `kubectl auth can-i <verb> <resource>` - Check if an action is allowed

## Troubleshooting & Debugging
- `kubectl get events --sort-by=.metadata.creationTimestamp` - Show events sorted by timestamp
- `kubectl get events -w` - Watch events in real-time
- `kubectl api-resources` - List all API resources
- `kubectl explain <resource>` - Get documentation for a resource

## Configuration & Context
- `kubectl config view` - Show merged kubeconfig settings
- `kubectl config get-contexts` - List all contexts
- `kubectl config use-context <context-name>` - Switch to another context
- `kubectl config current-context` - Show current context

## YAML Operations
- `kubectl apply -f <file.yaml>` - Apply configuration from a YAML file
- `kubectl delete -f <file.yaml>` - Delete resources defined in a YAML file
- `kubectl get <resource> <name> -o yaml` - Get resource configuration in YAML format
- `kubectl get <resource> <name> -o json` - Get resource configuration in JSON format

## Custom Columns & Output Formatting
- `kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName` - Custom columns output
- `kubectl get pods --sort-by=.metadata.creationTimestamp` - Sort by creation time
- `kubectl get pods --field-selector=status.phase=Running` - Filter by field selector