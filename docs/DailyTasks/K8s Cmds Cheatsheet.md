## Cluster Management
- `k cluster-info` - Display cluster information
- `k get nodes` - List all nodes in the cluster
- `k describe node <node-name>` - Show detailed information about a specific node
- `k top node` - Show resource usage (CPU/Memory) for nodes
- `k top pod` - Show resource usage for pods
- `k cordon <node-name>` - Mark node as unschedulable
- `k uncordon <node-name>` - Mark node as schedulable
- `k drain <node-name>` - Drain node in preparation for maintenance

# Apply and Remove Labels

- `k label <resource-type> <resource-name> <key>=<value> --overwrite`
- `k label pod mypod app=nginx --overwrite` - apply label
- `k label namespace namespace-b name=namespace-b` 

- `k label <resource-type> <resource-name> <key>-`
- `k label pod mypod app-` - Remove label
- `k label node <node-name> node-role.kubernetes.io/infra=""` - Label a node as an infra node
- `k get nodes --show-labels` - to see all labels on nodes(specific resources)\
- 
# Apply a taint to an infra node

- `k adm taint node <node-name> node-role.kubernetes.io/infra:NoSchedule` - apply taint on infra node

## Namespace Operations
- `k get namespaces` - List all namespaces
- `k create namespace <namespace-name>` - Create a new namespace
- `k config set-context --current --namespace=<namespace-name>` - Set default namespace for current context
- `k delete namespace <namespace-name>` - Delete a namespace

## Pod Operations
- `k get pods` - List all pods in current namespace
- `k get pods -A` - List all pods in all namespaces
- `k get pods -o wide` - List pods with additional details (IP, node)
- `k describe pod <pod-name>` - Show detailed information about a pod
- `k logs <pod-name>` - Print pod logs
- `k logs -f <pod-name>` - Stream pod logs (follow)
- `k logs <pod-name> -c <container-name>` - Print logs from a specific container in a pod
- `k exec -it <pod-name> -- /bin/bash` - Execute a command in a pod (interactive)
- `k delete pod <pod-name>` - Delete a pod
- `k port-forward <pod-name> <local-port>:<pod-port>` - Forward a local port to a pod

## Deployment Operations
- `k get deployments` - List all deployments
- `k describe deployment <deployment-name>` - Show deployment details
- `k create deployment <name> --image=<image>` - Create a deployment
- `k scale deployment <deployment-name> --replicas=<number>` - Scale a deployment
- `k rollout status deployment/<deployment-name>` - Check rollout status
- `k rollout history deployment/<deployment-name>` - View rollout history
- `k rollout undo deployment/<deployment-name>` - Rollback to previous version
- `k rollout undo deployment/<deployment-name> --to-revision=<number>` - Rollback to specific revision
- `k set image deployment/<deployment-name> <container-name>=<new-image>` - Update deployment image

## Service Operations
- `k get services` - List all services
- `k describe service <service-name>` - Show service details
- `k expose deployment <deployment-name> --port=<port> --target-port=<target-port> --type=<type>` - Expose a deployment as a service
- `k delete service <service-name>` - Delete a service

## ConfigMap & Secrets
- `k get configmaps` - List all configmaps
- `k create configmap <name> --from-file=<path-to-file>` - Create configmap from file
- `k create configmap <name> --from-literal=<key>=<value>` - Create configmap from literal
- `k get secrets` - List all secrets
- `k create secret generic <name> --from-literal=<key>=<value>` - Create secret from literal
- `k create secret generic <name> --from-file=<path-to-file>` - Create secret from file

## StatefulSets & DaemonSets
- `k get statefulsets` - List all statefulsets
- `k get daemonsets` - List all daemonsets

## Jobs & CronJobs
- `k get jobs` - List all jobs
- `k get cronjobs` - List all cronjobs

## Persistent Volumes & Claims
- `k get pv` - List persistent volumes
- `k get pvc` - List persistent volume claims

## RBAC & Security
- `k get roles` - List roles
- `k get rolebindings` - List role bindings
- `k get clusterroles` - List cluster roles
- `k get clusterrolebindings` - List cluster role bindings
- `k auth can-i <verb> <resource>` - Check if an action is allowed

## Troubleshooting & Debugging
- `k get events --sort-by=.metadata.creationTimestamp` - Show events sorted by timestamp
- `k get events -w` - Watch events in real-time
- `k api-resources` - List all API resources
- `k explain <resource>` - Get documentation for a resource

## Configuration & Context
- `k config view` - Show merged kubeconfig settings
- `k config get-contexts` - List all contexts
- `k config use-context <context-name>` - Switch to another context
- `k config current-context` - Show current context

## YAML Operations
- `k apply -f <file.yaml>` - Apply configuration from a YAML file
- `k delete -f <file.yaml>` - Delete resources defined in a YAML file
- `k get <resource> <name> -o yaml` - Get resource configuration in YAML format
- `k get <resource> <name> -o json` - Get resource configuration in JSON format

## Custom Columns & Output Formatting
- `k get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName` - Custom columns output
- `k get pods --sort-by=.metadata.creationTimestamp` - Sort by creation time
- `k get pods --field-selector=status.phase=Running` - Filter by field selector