<span style="color:#4caf50;"><b>Created:</b> 2025-06-30</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
Great! Let’s configure **ArgoCD with HTTPS using `cert-manager`** for automatic TLS certificates (via Let’s Encrypt) in **k3s (Traefik)**.  

### **Step 1: Install Cert-Manager**
```bash
# Install cert-manager (adjust version if needed)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.3/cert-manager.yaml
```
Verify installation:
```bash
kubectl get pods -n cert-manager

gouse@gouse:~$ kubectl get pods -n cert-manager -w
NAME                                       READY   STATUS    RESTARTS   AGE
cert-manager-776494b6cf-xb6dc              1/1     Running   0          20s
cert-manager-cainjector-6cf76fc759-9267r   1/1     Running   0          20s
cert-manager-webhook-7bfbfdc97c-g4btd      1/1     Running   0          19s
```

### **Step 2: Configure Let’s Encrypt Issuer**
Create a `ClusterIssuer` for Let’s Encrypt (replace `your-email@example.com`):  
**File:** `letsencrypt-issuer.yaml`

```
gouse@gouse:~$ k api-resources | grep ClusterIssuer
clusterissuers      cert-manager.io/v1    false     ClusterIssuer
```

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    email: your-email@example.com
    server: https://acme-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      name: letsencrypt-prod-account-key
    solvers:
    - http01:
        ingress:
          class: traefik  # k3s uses Traefik by default
```
Apply:
```bash
kubectl apply -f letsencrypt-issuer.yaml

gouse@gouse:~/DevOps/multipass_scripts/argocd$ kubectl apply -f letsencrypt-issuer.yaml
clusterissuer.cert-manager.io/letsencrypt-prod created

gouse@gouse:~/DevOps/multipass_scripts/argocd$ k get clusterissuer.cert-manager.io/letsencrypt-prod
NAME               READY   AGE
letsencrypt-prod   False   23s
```

### **Step 3: Deploy ArgoCD (Skip if Already Done)**
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### **Step 4: Create Ingress with TLS Automation**
**File:** `argocd-ingress-tls.yaml`  
Replace `argocd.yourdomain.com` with your actual domain (must resolve to your k3s IP).  
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: argocd-ingress
  namespace: argocd
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod  # Refers to ClusterIssuer
    traefik.ingress.kubernetes.io/router.entrypoints: websecure
    traefik.ingress.kubernetes.io/router.tls: "true"
spec:
  tls:
  - hosts:
    - argocd.local.com   # Your domain here
    secretName: argocd-tls    # cert-manager stores cert here
  rules:
  - host: argocd.local.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: argocd-server
            port:
              number: 443     # ArgoCD's HTTPS port
```
Apply:
```bash
kubectl apply -f argocd-ingress-tls.yaml

gouse@gouse:~/DevOps/multipass_scripts/argocd$ kubectl apply -f argocd-ingress-tls.yaml
ingress.networking.k8s.io/argocd-ingress created

gouse@gouse:~/DevOps/multipass_scripts/argocd$ k get ingress.networking.k8s.io/argocd-ingress -n argocd
NAME             CLASS     HOSTS              ADDRESS                                                  PORTS     AGE
argocd-ingress   traefik   argocd.local.com   10.94.226.136,10.94.226.145,10.94.226.164,10.94.226.18   80, 443   32s
```

### **Step 5: Verify TLS Certificate**
Check certificate status:
```bash
kubectl get certificate -n argocd

gouse@gouse:~/DevOps/multipass_scripts/argocd$ kubectl get certificate -n argocd
NAME         READY   SECRET       AGE
argocd-tls   False   argocd-tls   65s
```
Once ready (status `True`), access ArgoCD securely:
```
https://argocd.yourdomain.com

https://argocd.local.com
```

### **Step 6: Get Admin Password**
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### **Key Notes**
1. **Domain Requirements**:  
   - Your domain (`argocd.yourdomain.com`) must point to the public IP of your k3s cluster.  
   - For local testing, use a DNS service like `nip.io` (e.g., `argocd.192-168-1-100.nip.io`).  

2. **Traefik + cert-manager**:  
   - cert-manager automatically creates a challenge (`HTTP01`) to verify domain ownership.  
   - Traefik routes the challenge to cert-manager for validation.  

3. **Production Security**:  
   - Use `letsencrypt-prod` (not staging) for trusted certs.  
   - Ensure ArgoCD’s admin password is rotated after setup.  

### **Troubleshooting**
- **Certificate not issued?**  
  Check challenges:  
  ```bash
  kubectl describe challenges -n argocd
  ```
- **Traefik not routing?**  
  Check logs:  
  ```bash
  kubectl logs -n kube-system -l app.kubernetes.io/name=traefik
  ```

Let me know if you need help debugging! 🛠️