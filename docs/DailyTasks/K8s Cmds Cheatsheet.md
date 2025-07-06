<span style="color:#4caf50;"><b>Created:</b> 2025-06-23</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
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

## Annotations
- `k annotate pod mypod key=value`
- `k annotate pod mypod owner="gowse" purpose="debugging"` - apply annotation
- `k annotate pod mypod purpose-` - Remove annotation
- `kubectl get pods -A -o json | jq -r '.items[] | select(.metadata.annotations["w3h.why"] == "debugging") | [.metadata.namespace, .metadata.name] | @tsv'`


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