<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
Your config file looks good, but I notice a few things to optimize. Here's an improved version with some corrections and the steps to deploy Traefik with dashboard access:

## 1. Updated k3d cluster config## 2. Create the cluster

create dev-cluster confi file to setup a cluster by disabling traefik 
```yaml
apiVersion: k3d.io/v1alpha5
kind: Simple
metadata:
  name: dev-cluster
servers: 1
agents: 2
ports:
  - port: 30907:30907    # Cyclops / Minio
    nodeFilters:
      - loadbalancer
  - port: 31446:31446    # Jenkins
    nodeFilters:
      - loadbalancer
  - port: 31447:31447    # ArgoCD
    nodeFilters:
      - loadbalancer
  - port: 31448:31448    # Gitea
    nodeFilters:
      - loadbalancer
  - port: 30080:80       # Ingress HTTP
    nodeFilters:
      - loadbalancer
  - port: 30443:443      # Ingress HTTPS
    nodeFilters:
      - loadbalancer
  - port: 31000:31000    # Longhorn UI (optional)
    nodeFilters:
      - loadbalancer
  - port: 30090:30090    # Prometheus (optional)
    nodeFilters:
      - loadbalancer
  - port: 30099:30099    # Grafana (optional) - Fixed port mapping
    nodeFilters:
      - loadbalancer
  - port: 30900:30900    # Traefik Dashboard - Fixed port mapping
    nodeFilters:
      - loadbalancer
options:
  k3s:
    extraArgs:
      - arg: --disable=traefik
        nodeFilters:
          - server:*
  kubeconfig:
    updateDefaultKubeconfig: true
    switchCurrentContext: true
```
create a cluster with this config file
```bash
k3d cluster create --config dev-cluster.yaml
```

## 3. Install Traefik using Helm

Since we're disabling the default k3s Traefik, we'll install it manually with custom configuration:

create helm traefik values:
```yaml
# Traefik Helm Chart Values
image:
  tag: "3.0"

deployment:
  replicas: 1

service:
  type: NodePort
  # Map standard ports
  ports:
    web:
      port: 80
      nodePort: 30080
    websecure:
      port: 443
      nodePort: 30443
    traefik:
      port: 9000
      expose: true
      nodePort: 30900

# Enable dashboard
ingressRoute:
  dashboard:
    enabled: true
    matchRule: Host(`traefik.localhost`) && (PathPrefix(`/dashboard`) || PathPrefix(`/api`))
    entryPoints: ["traefik"]

# API and Dashboard settings
api:
  dashboard: true
  debug: true
  insecure: true  # For development only

# Logs
logs:
  general:
    level: INFO
  access:
    enabled: true

# Enable providers
providers:
  kubernetesCRD:
    enabled: true
    allowCrossNamespace: true
  kubernetesIngress:
    enabled: true

# Global arguments
globalArguments:
  - "--api.insecure=true"
  - "--api.dashboard=true"

# Additional arguments
additionalArguments:
  - "--log.level=INFO"
  - "--accesslog=true"
  - "--metrics.prometheus=true"
  - "--metrics.prometheus.entryPoint=metrics"

# Prometheus metrics
metrics:
  prometheus:
    entryPoint: metrics
    
# Enable persistent storage for certificates (optional)
persistence:
  enabled: false
```

````bash
# Add Traefik Helm repository
helm repo add traefik https://traefik.github.io/charts
helm repo update

# Create namespace
kubectl create namespace traefik-system

# Create Traefik values file
## 4. Install Traefik

helm install traefik traefik/traefik \
  --namespace traefik-system \
  --values traefik-values.yaml \
  --wait
````

## 5. Verify Traefik installation

```bash
# Check pods
kubectl get pods -n traefik-system

# Check services
kubectl get svc -n traefik-system

# Check if dashboard is accessible
curl http://localhost:30900/dashboard/
# checked not accessible, getting below error
gouse@gouse:~$ curl http://localhost:30900/dashboard/
curl: (52) Empty reply from server
```

## 6. Create an IngressRoute for easier dashboard access (optional)Apply the IngressRoute:

create traefik dashboard ingress route traefik-dashboard-ingress.yaml
```
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: traefik-dashboard
  namespace: traefik-system
spec:
  entryPoints:
    - web
  routes:
    - match: Host(`traefik.dev.local`)
      kind: Rule
      services:
        - name: api@internal
          kind: TraefikService
---
# Optional: Middleware for basic auth
apiVersion: v1
kind: Secret
metadata:
  name: traefik-dashboard-auth
  namespace: traefik-system
type: kubernetes.io/basic-auth
stringData:
  username: admin
  password: changeme
---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: traefik-dashboard-auth
  namespace: traefik-system
spec:
  basicAuth:
    secret: traefik-dashboard-auth
```

```bash
kubectl apply -f traefik-dashboard-ingress.yaml

gouse@gouse:~/DevOps/k3d$ kubectl apply -f traefik-dashboard-ingress.yaml
Warning: resource ingressroutes/traefik-dashboard is missing the kubectl.kubernetes.io/last-applied-configuration annotation which is required by kubectl apply. kubectl apply should only be used on resources created declaratively by either kubectl create --save-config or kubectl apply. The missing annotation will be patched automatically.
ingressroute.traefik.io/traefik-dashboard configured
secret/traefik-dashboard-auth created
middleware.traefik.io/traefik-dashboard-auth created
```

## 7. Access the Traefik Dashboard

You can now access the Traefik dashboard in multiple ways:

1. **Direct NodePort access**: http://localhost:30900/dashboard/
```html
in browser, it tried but getting as below

# The connection was reset
The connection to the server was reset while the page was loading.
```
1. **Via Ingress** (if you added the host to /etc/hosts): http://traefik.dev.local

## 8. Deploy a sample application to test TraefikDeploy the sample app:

create a sample app:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: whoami
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: whoami
  template:
    metadata:
      labels:
        app: whoami
    spec:
      containers:
      - name: whoami
        image: traefik/whoami
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: whoami
  namespace: default
spec:
  selector:
    app: whoami
  ports:
    - port: 80
      targetPort: 80
---
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: whoami
  namespace: default
spec:
  entryPoints:
    - web
  routes:
    - match: Host(`whoami.dev.local`)
      kind: Rule
      services:
        - name: whoami
          port: 80
```

```bash
kubectl apply -f sample-app.yaml
```

## Important Notes:

1. **Port mappings**: I fixed the port mappings for Grafana and Traefik dashboard. They should map to the same ports (30099:30099 and 30900:30900).
    
2. **Traefik installation**: Since k3s comes with Traefik by default, I added the `--disable=traefik` flag to install our own version with custom configuration.
    
3. **Dashboard access**: The dashboard will be available at http://localhost:30900/dashboard/ (note the trailing slash).
    
4. **Security**: For production, always secure the dashboard with authentication and use HTTPS.
    
5. **Host entries**: Add these to your `/etc/hosts` file for easier access:
    
    ```
    127.0.0.1 traefik.dev.local
    127.0.0.1 whoami.dev.local
    ```
    

This setup gives you full control over Traefik configuration and makes it easy to add more services with their respective ingress routes.

# post above setup, my observations on not working

```json
in my k3d conifg file i routed with below details for traefik - port: 30900:30900 # Traefik Dashboard - Fixed port mapping nodeFilters: - loadbalancer

but created service with different port, i think this is the issue which not able to access the curl [http://localhost:30900/dashboard/](http://localhost:30900/dashboard/) curl: (52) Empty reply from server

$ kubectl get svc -n traefik-system NAME TYPE CLUSTER-IP EXTERNAL-IP PORT(S) AGE traefik NodePort 10.43.48.148 <none> 80:32560/TCP,443:31788/TCP 22m

and also i added values in /etc/hosts 127.0.0.1 traefik.dev.local 127.0.0.1 whoami.dev.local

and i think it should be loadbalancer instead of nodeport for traefik-system svc what could be the issue, that i have not able to access
```

You're absolutely right! The issue is that the Traefik service isn't exposing port 9000 (the dashboard port) and the NodePort mappings don't match your k3d configuration. Let's fix this:

## 1. First, let's check the current Traefik service configuration:

```bash
kubectl get svc traefik -n traefik-system -o yaml
```

## 2. Update the Traefik values file to properly expose the dashboard port:## 3. Upgrade Traefik with the corrected configuration:

update traefik-values-fixed.yaml
```
# Traefik Helm Chart Values - Fixed Schema
image:
  tag: "3.0"

deployment:
  replicas: 1

service:
  type: NodePort
  spec: {}
  
ports:
  web:
    port: 8000
    expose:
      default: true
    exposedPort: 80
    nodePort: 30080
    protocol: TCP
  websecure:
    port: 8443
    expose:
      default: true
    exposedPort: 443
    nodePort: 30443
    protocol: TCP
  traefik:
    port: 9000
    expose:
      default: true
    exposedPort: 9000
    nodePort: 30900
    protocol: TCP

# Enable dashboard
ingressRoute:
  dashboard:
    enabled: true
    matchRule: PathPrefix(`/dashboard`) || PathPrefix(`/api`)
    entryPoints: ["traefik"]

# API and Dashboard settings
api:
  dashboard: true
  debug: true
  insecure: true  # For development only

# Logs
logs:
  general:
    level: INFO
  access:
    enabled: true

# Enable providers
providers:
  kubernetesCRD:
    enabled: true
    allowCrossNamespace: true
  kubernetesIngress:
    enabled: true

# Global arguments
globalArguments:
  - "--api.insecure=true"
  - "--api.dashboard=true"

# Additional arguments
additionalArguments:
  - "--log.level=INFO"
  - "--accesslog=true"

# Enable persistent storage for certificates (optional)
persistence:
  enabled: false
```

```bash
helm upgrade traefik traefik/traefik \
  --namespace traefik-system \
  --values traefik-values-fixed.yaml \
  --wait
```

```json
$ helm upgrade traefik traefik/traefik   --namespace traefik-system   --values traefik-values-fixed.yaml   --wait
Release "traefik" has been upgraded. Happy Helming!
NAME: traefik
LAST DEPLOYED: Sat Jun  7 11:15:27 2025
NAMESPACE: traefik-system
STATUS: deployed
REVISION: 2
TEST SUITE: None
NOTES:
traefik with docker.io/traefik:3.0 has been deployed successfully on traefik-system namespace !
```

## 4. If the above doesn't work (k3d sometimes has issues with LoadBalancer type), let's patch the service directly:Apply the patch:

```bash
kubectl apply -f traefik-service-patch.yaml
```

## 5. Alternative: Create a separate service for the dashboard:```bash

kubectl apply -f traefik-dashboard-service.yaml

````

## 6. Verify the service has the correct ports:

```bash
# Check services
kubectl get svc -n traefik-system

# You should see something like:
# NAME                TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)                                     AGE
# traefik             NodePort   10.43.48.148    <none>        80:30080/TCP,443:30443/TCP,9000:30900/TCP  22m
````

## 7. Check if Traefik pod is exposing port 9000:

```bash
# Get pod name
kubectl get pods -n traefik-system

# Check if port 9000 is exposed
kubectl describe pod -n traefik-system <traefik-pod-name> | grep -A 5 "Ports:"
```

## 8. Test access again:

```bash
# Direct dashboard access
curl http://localhost:30900/dashboard/

# Or check the API endpoint
curl http://localhost:30900/api/rawdata
```

## 9. If still having issues, check Traefik logs:

```bash
kubectl logs -n traefik-system -l app.kubernetes.io/name=traefik -f
```

## Quick Debug Commands:

```bash
# Check if the port is actually listening
kubectl exec -n traefik-system deployment/traefik -- netstat -tlnp | grep 9000

# Port forward directly to test
kubectl port-forward -n traefik-system deployment/traefik 9000:9000
# Then try: curl http://localhost:9000/dashboard/
```

The main issue was that the Traefik service wasn't configured to expose port 9000 with the correct NodePort (30900) that matches your k3d configuration. The above solutions should fix this issue.

Still not working:
```json
https://traefik.dev.local:30900/dashboard/` also getting 404 error
```

# Check Traefik deployment arguments:

```
kubectl get deployment traefik -n traefik-system -o yaml | grep -A 30 "args:"
```

# If dashboard is not enabled, let's force enable it:
create a script and check
```bash
#!/bin/bash

# Patch Traefik deployment to ensure dashboard is enabled
kubectl patch deployment traefik -n traefik-system --type='json' -p='[
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/args/-",
    "value": "--api.dashboard=true"
  },
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/args/-",
    "value": "--api.insecure=true"
  },
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/args/-",
    "value": "--api.debug=true"
  }
]'

# Wait for rollout
kubectl rollout status deployment/traefik -n traefik-system

# Check the service has the traefik port
kubectl get svc traefik -n traefik-system -o jsonpath='{.spec.ports[?(@.name=="traefik")].nodePort}'
```

## Summary:

**DO NOT USE**: `https://traefik.dev.local:30900/dashboard/`

**USE ONE OF THESE**:

- `http://localhost:30900/dashboard/` (direct dashboard access)
- `http://traefik.dev.local:30080/` (through ingress HTTP)
- `https://traefik.dev.local:30443/` (through ingress HTTPS)

The key is understanding that:

- Port 30900 = Direct dashboard port (use with localhost)
- Port 30080/30443 = Ingress ports (use with domain names)