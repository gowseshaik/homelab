## Prerequisites

- 1. Kubernetes cluster up and running
- 2. `kubectl` configured to access the cluster
- 3. `kubeseal` CLI installed locally ([Install guide](https://github.com/bitnami-labs/sealed-secrets#install))
- 4. Git repository for your manifests (GitHub, Gitea, etc.)
- 5. Sealed Secrets controller installed in the cluster

## Step 1: Install Sealed Secrets Controller

```bash
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/latest/download/controller.yaml
```

This installs the controller pod that will decrypt sealed secrets inside the cluster.

---

## Step 2: Create Plain Kubernetes Secret and ConfigMap Files

Create files locally for your app configuration.

**configmap.yaml**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: default
data:
  DB_HOST: "db.example.com"
  DB_PORT: "5432"
```

**secret.yaml**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
  namespace: default
type: Opaque
data:
  username: YWRtaW4=       # base64 encoded 'admin'
  password: cGFzc3dvcmQ=   # base64 encoded 'password'
```

---

## Step 3: Seal the ConfigMap and Secret Locally

Use `kubeseal` to encrypt your plain secrets before pushing to Git.

```bash
kubectl create -f configmap.yaml --dry-run=client -o json | kubeseal --format yaml > sealed-configmap.yaml
kubectl create -f secret.yaml --dry-run=client -o json | kubeseal --format yaml > sealed-secret.yaml
```

Now you have **sealed-configmap.yaml** and **sealed-secret.yaml** with encrypted data safe for Git.

---

## Step 4: Add Sealed Secrets Manifests to Git Repository

```bash
git clone git@github.com:youruser/yourrepo.git
cd yourrepo

mkdir -p k8s/secrets
cp ../sealed-configmap.yaml k8s/secrets/
cp ../sealed-secret.yaml k8s/secrets/

git add k8s/secrets/sealed-*.yaml
git commit -m "Add sealed ConfigMap and Secret for app"
git push origin main
```

---

## Step 5: Deployment YAML Referring to Secrets and ConfigMaps

Create or update your deployment manifest to inject env vars from ConfigMap and Secret.

**deployment.yaml**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: express-app
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: express-app
  template:
    metadata:
      labels:
        app: express-app
    spec:
      containers:
      - name: express-app
        image: your-image:latest
        env:
        - name: DB_HOST
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: DB_HOST
        - name: DB_PORT
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: DB_PORT
        - name: DB_USER
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: username
        - name: DB_PASS
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: password
```

Add this deployment manifest to Git repo alongside sealed secrets:

```bash
cp ../deployment.yaml k8s/deployments/
git add k8s/deployments/deployment.yaml
git commit -m "Add deployment for express app"
git push origin main
```

---

## Step 6: Use GitOps Tool to Sync Repo to Cluster

Use ArgoCD, Flux, or manual `kubectl apply -f` on the repo manifests:

```bash
kubectl apply -f k8s/secrets/sealed-configmap.yaml
kubectl apply -f k8s/secrets/sealed-secret.yaml
kubectl apply -f k8s/deployments/deployment.yaml
```

The Sealed Secrets controller will automatically decrypt sealed secrets and create normal Kubernetes Secret and ConfigMap objects.

---

## Step 7: Application Reads Environment Variables

Your Node.js app code reads env vars:

```js
const config = {
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || '5432',
  user: process.env.DB_USER || 'user',
  pass: process.env.DB_PASS || 'pass',
};
```

---

## Summary

|Step|Description|
|---|---|
|1|Install Sealed Secrets controller in cluster|
|2|Create plain ConfigMap and Secret YAML files|
|3|Seal files with `kubeseal` CLI locally|
|4|Commit sealed secrets YAML to Git repo|
|5|Create deployment manifest using secrets/config|
|6|GitOps sync or manual apply to Kubernetes|
|7|App uses env variables from Kubernetes Secrets|
