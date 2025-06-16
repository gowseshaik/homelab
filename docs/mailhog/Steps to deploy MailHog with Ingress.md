Here are the **full steps** to deploy **MailHog with Ingress via Traefik** on a **k3d cluster** using port 80.

---

### ✅ Step 1: Create `k3d` cluster with port 80 mapped

```yaml
# file: k3d-mailhog.yaml
apiVersion: k3d.io/v1alpha4
kind: Simple
name: mailhog-cluster
ports:
  - port: 80:80      # maps host port 80 to container port 80
    nodeFilters:
      - loadbalancer
```

```bash
k3d cluster create --config k3d-mailhog.yaml
```

---

### ✅ Step 2: Deploy Traefik (if not already)

Traefik is installed by default with `k3d`. Check with:

```bash
kubectl get pods -n kube-system | grep traefik
```

If not, install manually via Helm or manifest.

---

### ✅ Step 3: Create MailHog Deployment and Service

```yaml
# file: mailhog-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mailhog
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mailhog
  template:
    metadata:
      labels:
        app: mailhog
    spec:
      containers:
      - name: mailhog
        image: mailhog/mailhog
        ports:
        - containerPort: 1025
        - containerPort: 8025 
---
apiVersion: v1
kind: Service
metadata:
  name: mailhog
spec:
  selector:
    app: mailhog
  ports:
  - name: smtp
    port: 1025
    targetPort: 1025
  - name: http
    port: 8025  # i used 80, becuase i used 80 in k3d config
    targetPort: 8025
```

```bash
kubectl apply -f mailhog-deployment.yaml
```

---

### ✅ Step 4: Create Ingress for Traefik

```yaml
# file: mailhog-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mailhog
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: web
spec:
  rules:
  - host: mailhog.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: mailhog
            port:
              number: 8025  # i used 80, becuase i used 80 in k3d config
```

```bash
kubectl apply -f mailhog-ingress.yaml
```

---

### ✅ Step 5: Add local DNS for `mailhog.local`

Edit `/etc/hosts`:

```
127.0.0.1 mailhog.local
```

---

### ✅ Step 6: Access MailHog

Open in browser:  
`http://mailhog.local` → Web UI  
SMTP will be available at `mailhog.local:1025` (for apps)

---

Let me know if you want the same with TLS (HTTPS) using Traefik + cert-manager.