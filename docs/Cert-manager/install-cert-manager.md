<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

Here are the **full steps to deploy MailHog with HTTPS (TLS) using Traefik + cert-manager** on a `k3d` cluster:

updated: 2025-07-06T12:mm:ssZ
author: Gouse Shaik
---

## ✅ Step 1: `k3d` Cluster with Port 80 & 443

```yaml
# k3d-mailhog.yaml
apiVersion: k3d.io/v1alpha4
kind: Simple
name: mailhog-tls
ports:
  - port: 80:80     # HTTP
    nodeFilters:
      - loadbalancer
  - port: 443:443   # HTTPS
    nodeFilters:
      - loadbalancer
```

```bash
k3d cluster create --config k3d-mailhog.yaml
```

---

## ✅ Step 2: Install `cert-manager`

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
```

Wait until all pods in `cert-manager` namespace are ready.

## ✅ Check TLS Certificate Secret Created?
```
kubectl get certificate
kubectl describe certificate mailhog-cert
kubectl get secret mailhog-tls


If all looks fine and still not working, paste the output of:
kubectl get ingress
kubectl describe ingress mailhog
kubectl get certificate
kubectl describe certificate mailhog-cert
```

---

## ✅ Step 3: Install `ClusterIssuer` (Self-Signed for Dev)

```yaml
# selfsigned-clusterissuer.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned-issuer
spec:
  selfSigned: {}
```

```bash
kubectl apply -f selfsigned-clusterissuer.yaml
```

---

## ✅ Step 4: Create TLS Certificate for `mailhog.local`

```yaml
# mailhog-cert.yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: mailhog-cert
spec:
  secretName: mailhog-tls
  dnsNames:
    - mailhog.local
  issuerRef:
    name: selfsigned-issuer
    kind: ClusterIssuer
  commonName: mailhog.local
```

```bash
kubectl apply -f mailhog-cert.yaml

gouse@gouse:~/DevOps/k3d$ k apply -f mailhog-cert.yaml 
Warning: spec.privateKey.rotationPolicy: In cert-manager >= v1.18.0, the default value changed from `Never` to `Always`.
certificate.cert-manager.io/mailhog-cert created
```

---

## ✅ Step 5: Deploy MailHog + Service

Same as before (`mailhog-deployment.yaml`):

```bash
kubectl apply -f mailhog-deployment.yaml
```

---

## ✅ Step 6: Create HTTPS Ingress with TLS

```yaml
# mailhog-ingress-tls.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mailhog
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: websecure
spec:
  tls:
  - hosts:
    - mailhog.local
    secretName: mailhog-tls
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
              number: 8025
```

```bash
kubectl apply -f mailhog-ingress-tls.yaml
```

---

## ✅ Step 7: Add to `/etc/hosts`

```
127.0.0.1 mailhog.local
```

---

## ✅ Step 8: Open in Browser

```
https://mailhog.local
```

You may need to accept the self-signed cert warning if using Chrome/Firefox.

---

Let me know if you want the same using **Let’s Encrypt** instead of self-signed.