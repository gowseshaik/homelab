Yes, you **can access the pods**, but **not via external IP** because it's a **headless service (`ClusterIP: None`)** — it only helps with **pod discovery**, not load balancing or external access.

```bash
gouse@gouse:~/DevOps/k3d$ kubectl run curlpod --rm -it --image=curlimages/curl -- /bin/sh
If you don't see a command prompt, try pressing enter.
~ $ curl nginx-0.nginx-headless.default.svc.cluster.local
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
~ $ exit
Session ended, resume using 'kubectl attach curlpod -c curlpod -i -t' command when the pod is running
pod "curlpod" deleted
```


---

### ✅ Ways to Access

#### 1. **From inside the cluster (e.g., debug pod):**

```bash
kubectl run curlpod --rm -it --image=curlimages/curl -- /bin/sh
```

Then try:

```bash
curl nginx-0.nginx-headless.default.svc.cluster.local
```

Or test all pods:

```bash
for i in 0 1 2; do curl nginx-$i.nginx-headless.default.svc.cluster.local; done
```

---

#### 2. **If you want external access**, expose with a regular service:

```bash
kubectl expose statefulset nginx --name=nginx-service --port=80 --target-port=80 --type=NodePort
```

Then get:

```bash
kubectl get svc nginx-service
```

Access via:

```bash
http://<NodeIP>:<NodePort>
```

---

You can also do and access this `statefulset` with `headless applicaiton` to access, if you want an `Ingress` setup or `LoadBalancer` type instead.