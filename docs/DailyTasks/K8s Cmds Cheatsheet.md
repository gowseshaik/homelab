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

## Node-role labels
#### Apply node-role label
- `k label node k3d-dev-cluster-agent-1 node-role.kubernetes.io/worker1=
#### Rmove node-role label
- `k label node k3d-dev-cluster-agent-1 node-role.kubernetes.io/worker1-`

## Labels

|**Command / Usage**|**Description**|
|---|---|
|`kubectl get pods --show-labels`|Show all labels for each pod|
|`kubectl get pods -l key=value`|Filter pods by label|
|`kubectl get pods -l 'key in (v1,v2)'`|Filter by label values (set-based)|
|`kubectl label pod <pod-name> key=value`|Add a label to a pod|
|`kubectl label pod <pod-name> key-`|Remove a label from a pod|
|`kubectl label --overwrite pod key=value`|Overwrite an existing label|
|`kubectl get pods --selector='env=prod'`|Another way to filter using a label selector|
|`kubectl describe pod <pod-name>`|View labels (under Metadata)|
|`kubectl get nodes --show-labels`|Show labels on nodes|
|`kubectl label nodes <node-name> key=value`|Add a label to a node|
|`kubectl label deployment <dep> key=value`|Add label to deployment|
|`kubectl get svc -l app=myapp`|Get services with specific label|
|`kubectl delete pod -l env=test`|Delete pods by label|
|`kubectl apply -f file.yaml`|Apply resource with labels defined in YAML|

Let me know if you want YAML examples or `taints`, `annotations` cheat sheet too.
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