To **confirm Ingress resources, routes, and active requests**, follow these steps:

---

### ✅ 1. **List All Ingress Resources**

```bash
kubectl get ingress -A
```

---

### ✅ 2. **Inspect Ingress Rules and Routes**

```bash
kubectl describe ingress <ingress-name> -n <namespace>
```

Look for:

- `Host`
    
- `Path`
    
- `Service Name`
    
- `IngressClassName`
    

---

### ✅ 3. **Check Ingress Controller Logs for Requests**

For **NGINX**:

```bash
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx
```

For **Traefik**:

```bash
kubectl logs -n kube-system -l app.kubernetes.io/name=traefik
```

For **Istio**:

```bash
kubectl logs -n istio-system -l app=istio-ingressgateway
```

---
Perfect — if **Traefik is already installed by default with K3d**, here's the minimal setup to route traffic **using ClusterIP services** like ALB:

---

## ✅ Use Default K3d Traefik with Ingress (ALB Style)

### **Step 1: exposing Traefik ports in k3d cluster config yaml file

You're exposing Traefik **port 80** to **host port `30080`** like this:
```
- port: 30080:80
  nodeFilters:
    - loadbalancer
```

### **Step 2: Deploy Sample App**
```bash
kubectl create namespace demo

kubectl create deployment whoami --image=traefik/whoami -n demo
kubectl expose deployment whoami --port=80 --name=whoami -n demo
```

> ✅ This app uses a `ClusterIP` service (default)

---

### **Step 3: Create Ingress Resource**

#whoami-ingress.yaml
```yaml
# whoami-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: whoami-ingress
  namespace: demo
spec:
  rules:
    - host: whoami.localhost
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: whoami
                port:
                  number: 80
```

Apply it:

```bash
kubectl apply -f whoami-ingress.yaml
```

```bash
gouse@gouse:~/DevOps/k3d$ k get ingress -A
NAMESPACE   NAME             CLASS     HOSTS              ADDRESS                            PORTS   AGE
demo        whoami-ingress   traefik   whoami.localhost   172.18.0.2,172.18.0.3,172.18.0.4   80      8m13s
```
---

### **Step 3: Add Host Mapping**

```bash
sudo echo "127.0.0.1 whoami.localhost" >> /etc/hosts # Localhost for homeLab

sudo echo "172.18.0.2 whoami.localhost" >> /etc/hosts # LoadBalancer IP for Production grade setup and configurations
```

---

### **Step 4: Access in Browser**

Open:  
**[http://whoami.localhost](http://whoami.localhost)**

---

### ⚠️ Optional: If Traefik Doesn't Route

Check if the default Traefik has IngressClass enabled:

```bash
kubectl get ingressclass
```

You should see something like:

```
NAME      CONTROLLER             PARAMETERS   AGE
traefik   traefik.io/ingress-controller   ...   ...
```

If not, you can **explicitly set it** in your Ingress:

```yaml
spec:
  ingressClassName: traefik
```

---

You're now running a **ClusterIP-only app with Ingress routing through default Traefik**, exactly like an AWS ALB setup. Let me know if you want TLS added.

Here's a **Traefik Dashboard Ingress manifest** for your **K3d setup** using existing port `30900:9000` (from your YAML) and **ClusterIP service**:

---

### ✅ `traefik-dashboard.yaml`

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: traefik-dashboard
  namespace: kube-system
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: web
spec:
  ingressClassName: traefik
  rules:
    - host: traefik.localhost
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: traefik
                port:
                  number: 9000
```

---

### ✅ `/etc/hosts` Entry

```bash
127.0.0.1 traefik.localhost
```

---

### ✅ Access Dashboard

```
http://traefik.localhost:30900
```

OR (if you prefer Ingress via port 80 → 30080):

```
http://traefik.localhost:30080
```

> In that case, change `port: 9000` to `port: 80` in the Ingress and make sure Traefik listens on web entrypoint for both.

---

Let me know which way you prefer:

- Direct: `30900`
    
- Through Ingress: `30080`  
    I’ll adjust the manifest accordingly.

