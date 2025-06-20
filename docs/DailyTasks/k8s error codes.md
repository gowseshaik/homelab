## HTTP Status Codes

| Code | Name | Description |
|------|------|-------------|
| 400 | Bad Request | Invalid request format or parameters |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Credentials accepted but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Request conflicts with current state |
| 422 | Unprocessable Entity | Valid request but semantic errors |
| 429 | Too Many Requests | Rate limiting applied |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Service not available |

## Common Pod/Container Errors

| Error Code/Message | Description |
|--------------------|-------------|
| CrashLoopBackOff | Container crashes repeatedly |
| ImagePullBackOff | Cannot pull container image |
| ErrImagePull | General image pull error |
| ImageInspectError | Cannot inspect container image |
| ErrNoFreePorts | No free ports available |
| CreateContainerConfigError | Problem with config (secrets, volumes) |
| CreateContainerError | General container creation error |
| RunContainerError | General container runtime error |
| OOMKilled | Out of Memory killed container |
| ContainerCreating | Stuck in creation phase |
| Terminating | Stuck in deletion phase |
| Pending | Not scheduled yet |
| Evicted | Node resource pressure |
| FailedMount | Volume mounting failed |
| FailedScheduling | Scheduler cannot place pod |

## Node Conditions

| Condition | Description |
|-----------|-------------|
| Ready | Node is healthy |
| MemoryPressure | Node memory is low |
| DiskPressure | Node disk space is low |
| PIDPressure | Too many processes |
| NetworkUnavailable | Network not configured |
| OutOfDisk | Node out of disk space |
| NotReady | Node not healthy |

## Common kubectl Errors

| Error | Description |
|-------|-------------|
| "connection refused" | Cannot connect to API server |
| "context deadline exceeded" | Request timeout |
| "the server doesn't have a resource type" | Resource type doesn't exist |
| "forbidden: User cannot..." | RBAC permission issue |
| "no matches for kind" | API version mismatch |
| "resource name may not be empty" | Missing resource name |
| "already exists" | Resource name conflict |

## Network Errors

| Error | Description |
|-------|-------------|
| NetworkPluginNotReady | CNI plugin not ready |
| FailedCreatePodSandBox | Container runtime network issue |
| FailedPortMapping | Port mapping failed |
| DNSConfigForming | DNS configuration error |
| NetworkNotReady | General network issue |

## Storage Errors

| Error | Description |
|-------|-------------|
| FailedAttachVolume | Cannot attach volume |
| FailedMount | Cannot mount volume |
| FailedUnMount | Cannot unmount volume |
| VolumeResizeFailed | Cannot resize volume |
| VolumeAlreadyExists | Volume name conflict |
| ProvisioningFailed | Storage provisioning failed |

## Troubleshooting Tips

1. **Check pod details**: `kubectl describe pod <pod-name>`
2. **Check pod logs**: `kubectl logs <pod-name> [-c container]`
3. **Check events**: `kubectl get events --sort-by=.metadata.creationTimestamp`
4. **Check node status**: `kubectl get nodes -o wide`
5. **Check component status**: `kubectl get cs`
6. **Check API health**: `kubectl get --raw /healthz`
7. **Check API versions**: `kubectl api-versions`

Remember that many errors will include additional details in their status messages that can help pinpoint the exact issue.