<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

Great! I'm glad it's working now. Let me provide you with a comprehensive, clean setup guide for Traefik with dashboard on k3d:This guide provides a complete, production-ready setup for Traefik on k3d. The key points to remember:

1. **Disable default k3s Traefik** to install your own version with full control
2. **Use NodePort service type** with specific port mappings matching your k3d config
3. **Enable dashboard explicitly** with `--api.dashboard=true` and `--api.insecure=true` flags
4. **Access patterns**:
    - Direct dashboard: `http://localhost:30900/dashboard/`
    - Through ingress: `http://traefik.localhost:30080/`
5. **Always include the trailing slash** when accessing `/dashboard/`

The setup is now modular and easy to extend with additional services, middleware, and security features. You can use this as a template for all your k3d clusters with Traefik.

# Complete Traefik Setup Guide for k3d

## Step 1: Create k3d Cluster Configuration

Create `dev-cluster.yaml`:

```yaml
apiVersion: k3d.io/v1alpha5
kind: Simple
metadata:
  name: dev-cluster
servers: 1
agents: 2
ports:
  - port: 30080:80       # Ingress HTTP
    nodeFilters:
      - loadbalancer
  - port: 30443:443      # Ingress HTTPS
    nodeFilters:
      - loadbalancer
  - port: 30900:9000     # Traefik Dashboard
    nodeFilters:
      - loadbalancer
  # Add your other application ports here
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

## Step 2: Create the Cluster

```bash
k3d cluster create --config dev-cluster.yaml
```

## Step 3: Install Traefik with Helm

### 3.1 Add Helm Repository

```bash
helm repo add traefik https://traefik.github.io/charts
helm repo update
```

### 3.2 Create Traefik Namespace

```bash
kubectl create namespace traefik-system
```

### 3.3 Create Traefik Values File

Create `traefik-values.yaml`:

```yaml
# Traefik Helm Chart Values
image:
  pullPolicy: IfNotPresent

deployment:
  enabled: true
  replicas: 1
  annotations: {}
  podAnnotations: {}
  additionalContainers: []
  initContainers: []

# Configure ports
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

# Service configuration
service:
  enabled: true
  type: NodePort
  annotations: {}
  labels: {}
  spec: {}
  loadBalancerSourceRanges: []
  externalIPs: []

# Enable dashboard
ingressRoute:
  dashboard:
    enabled: true
    annotations: {}
    labels: {}

# API and Dashboard settings
api:
  dashboard: true
  debug: true
  insecure: true

# Configure providers
providers:
  kubernetesCRD:
    enabled: true
    allowCrossNamespace: true
    allowExternalNameServices: true
    allowEmptyServices: true
  kubernetesIngress:
    enabled: true
    allowExternalNameServices: true
    allowEmptyServices: true

# Logs
logs:
  general:
    level: INFO
  access:
    enabled: true

# Global arguments
globalArguments:
  - "--global.checknewversion=false"
  - "--global.sendanonymoususage=false"

# Additional arguments
additionalArguments:
  - "--api.dashboard=true"
  - "--api.insecure=true"
  - "--log.level=INFO"
  - "--accesslog=true"
  - "--entrypoints.web.http.redirections.entrypoint.to=websecure"
  - "--entrypoints.web.http.redirections.entrypoint.scheme=https"

# Enable persistent storage for acme certificates
persistence:
  enabled: false
  name: data
  accessMode: ReadWriteOnce
  size: 128Mi
  storageClass: ""
  path: /data
  annotations: {}

# Security configurations
podSecurityContext:
  fsGroup: 65532

securityContext:
  capabilities:
    drop: [ALL]
  readOnlyRootFilesystem: true
  runAsGroup: 65532
  runAsNonRoot: true
  runAsUser: 65532
```

### 3.4 Install Traefik

```bash
helm install traefik traefik/traefik \
  --namespace traefik-system \
  --values traefik-values.yaml \
  --wait
```

## Step 4: Configure Dashboard Access

### 4.1 Create IngressRoute for Dashboard

Create `traefik-dashboard-ingress.yaml`:

```yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: traefik-dashboard
  namespace: traefik-system
  annotations:
    kubernetes.io/ingress.class: traefik
spec:
  entryPoints:
    - web
  routes:
    - match: Host(`traefik.localhost`) && (PathPrefix(`/dashboard`) || PathPrefix(`/api`))
      kind: Rule
      services:
        - name: api@internal
          kind: TraefikService
```

Apply the configuration:

```bash
kubectl apply -f traefik-dashboard-ingress.yaml
```

### 4.2 (Optional) Secure Dashboard with Basic Auth

Generate password:

```bash
# Generate password (replace 'admin' and 'your-password')
htpasswd -nb admin your-password | base64
```

Create `traefik-dashboard-auth.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: traefik-dashboard-auth
  namespace: traefik-system
data:
  users: |
    <base64-encoded-htpasswd-output>
---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: traefik-dashboard-auth
  namespace: traefik-system
spec:
  basicAuth:
    secret: traefik-dashboard-auth
---
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: traefik-dashboard-secure
  namespace: traefik-system
spec:
  entryPoints:
    - web
  routes:
    - match: Host(`traefik.localhost`) && (PathPrefix(`/dashboard`) || PathPrefix(`/api`))
      kind: Rule
      middlewares:
        - name: traefik-dashboard-auth
      services:
        - name: api@internal
          kind: TraefikService
```

Apply authentication:

```bash
kubectl apply -f traefik-dashboard-auth.yaml
```

## Step 5: Configure DNS (Optional)

Add to `/etc/hosts`:

```bash
127.0.0.1 traefik.localhost
127.0.0.1 app.localhost
# Add other domains as needed
```

## Step 6: Deploy Sample Application

Create `whoami-app.yaml`:

```yaml
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
    - match: Host(`whoami.localhost`)
      kind: Rule
      services:
        - name: whoami
          port: 80
```

Deploy the application:

```bash
kubectl apply -f whoami-app.yaml
```

## Step 7: Access Methods

### Dashboard Access:

- **Direct Port**: http://localhost:30900/dashboard/
- **Via Ingress**: http://traefik.localhost:30080/dashboard/

### Application Access:

- **Via Ingress**: http://whoami.localhost:30080/

## Step 8: Useful Commands

### Check Traefik Status:

```bash
# Check pods
kubectl get pods -n traefik-system

# Check services
kubectl get svc -n traefik-system

# Check logs
kubectl logs -n traefik-system -l app.kubernetes.io/name=traefik -f

# Check IngressRoutes
kubectl get ingressroute -A
```

### Debug Commands:

```bash
# Check if dashboard is accessible
curl http://localhost:30900/api/overview

# Test ingress routing
curl -H "Host: whoami.localhost" http://localhost:30080/

# Port forward for debugging
kubectl port-forward -n traefik-system deployment/traefik 9000:9000
```

## Step 9: Common Middleware Examples

### Rate Limiting:

```yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: rate-limit
spec:
  rateLimit:
    average: 100
    burst: 50
```

### Headers:

```yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: security-headers
spec:
  headers:
    frameDeny: true
    sslRedirect: true
    browserXssFilter: true
    contentTypeNosniff: true
```

### Redirect:

```yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: redirect-https
spec:
  redirectScheme:
    scheme: https
    permanent: true
```

## Troubleshooting

### Dashboard Not Accessible:

1. Check if the service has port 9000 exposed:
    
    ```bash
    kubectl get svc traefik -n traefik-system -o yaml | grep -A 5 "port: 9000"
    ```
    
2. Verify dashboard is enabled:
    
    ```bash
    kubectl get deployment traefik -n traefik-system -o yaml | grep -E "(dashboard|insecure)"
    ```
    
3. Check endpoints:
    
    ```bash
    kubectl get endpoints -n traefik-system
    ```
    

### Ingress Not Working:

1. Check IngressRoute:
    
    ```bash
    kubectl describe ingressroute -n <namespace> <name>
    ```
    
2. Check Traefik logs for errors:
    
    ```bash
    kubectl logs -n traefik-system -l app.kubernetes.io/name=traefik --tail=100
    ```
    

## Best Practices

1. **Always use HTTPS in production** - Configure proper TLS certificates
2. **Secure the dashboard** - Use authentication middleware
3. **Use namespaces** - Organize your IngressRoutes by namespace
4. **Monitor logs** - Set up proper logging and monitoring
5. **Resource limits** - Set appropriate resource requests and limits
6. **Regular updates** - Keep Traefik updated for security patches

This setup provides a solid foundation for using Traefik in your k3d development environment!