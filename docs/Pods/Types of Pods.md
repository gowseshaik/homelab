
|**Type**|**Description**|
|---|---|
|**Single Container Pod**|Most basic pod, runs one container.|
|**Multi-Container Pod**|Pod with multiple containers sharing the same network/storage (sidecar pattern).|
|**Init Container Pod**|Pod that runs init containers **before** main containers start.|
|**Static Pod**|Managed by **kubelet** directly (not via API server), used in control plane nodes.|
|**DaemonSet Pod**|Runs one pod per node, ideal for logs/metrics collection (e.g., Fluentd, Prometheus node-exporter).|
|**Deployment Pod**|Created and managed by a Deployment object for rolling updates and scaling.|
|**StatefulSet Pod**|Used for stateful apps, gives stable hostname and storage (e.g., databases).|
|**Job/ CronJob Pod**|Runs to completion once (Job) or on schedule (CronJob).|
|**Ephemeral Container Pod**|Used for debugging, doesn't run app logic, added dynamically.|
|**Mirror Pod**|Clone of a static pod, visible to the API server for monitoring.|
### 1. **Single Container Pod**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx
    image: nginx
```

🧾 _Use Case_: Simple stateless app or test container.

---

### 2. **Multi-Container Pod**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-pod
spec:
  containers:
  - name: app
    image: nginx
  - name: sidecar
    image: busybox
    command: ["sh", "-c", "while true; do echo Sidecar; sleep 30; done"]
```

🧾 _Use Case_: Log agent or proxy sidecar with main app.

---

### 3. **Init Container Pod**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: init-pod
spec:
  initContainers:
  - name: init
    image: busybox
    command: ["sh", "-c", "echo initializing... && sleep 10"]
  containers:
  - name: app
    image: nginx
```

🧾 _Use Case_: Pre-setup before app starts (e.g., config fetch, wait for DB).

---

### 4. **Static Pod**

- Save this to `/etc/kubernetes/manifests/static-nginx.yaml`:
    

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: static-nginx
spec:
  containers:
  - name: nginx
    image: nginx
```

🧾 _Use Case_: Run core components (like etcd, controller) outside of scheduler.

---

### 5. **DaemonSet Pod**

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-logger
spec:
  selector:
    matchLabels:
      app: logger
  template:
    metadata:
      labels:
        app: logger
    spec:
      containers:
      - name: log-agent
        image: fluentd
```

🧾 _Use Case_: Run log collector or monitoring agent on every node.

---

### 6. **Deployment Pod**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deploy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx
```

🧾 _Use Case_: Scalable, rolling update-ready web apps or APIs.

---

### 7. **StatefulSet Pod**

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
spec:
  serviceName: "mysql"
  replicas: 2
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:5.7
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: root
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
```

🧾 _Use Case_: Databases, message brokers needing persistent identity & storage.

---

### 8. **Job Pod**

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: one-time-job
spec:
  template:
    spec:
      containers:
      - name: pi
        image: perl
        command: ["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
```

🧾 _Use Case_: One-time batch job (like data migration, backup).

---

### 9. **CronJob Pod**

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: hello-cron
spec:
  schedule: "*/5 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: hello
            image: busybox
            command: ["sh", "-c", "date; echo Hello"]
          restartPolicy: OnFailure
```

🧾 _Use Case_: Scheduled tasks (e.g., cleanup, backups, reports).

---

### 10. **Ephemeral Container**

```bash
kubectl debug -it mypod --image=busybox --target=app -- /bin/sh
```

🧾 _Use Case_: On-demand debugging of a running pod (no restart needed).

# mirror pod
- 🧠 You **create a static pod** ✅ _Actual pod running on the node_
- **YAML Location**: Saved under `--pod-manifest-path` (e.g., `/etc/kubernetes/manifests`)
- 🧑‍💻 Kubelet runs it
- 📡 Kubelet then **informs the API server**, which **shows it as a mirror pod**, 
- ❌ _Not actually running_, it's just a _representation_ of the static pod

❌ Static Pod ≠ Mirror Pod  
✅ Static Pod → creates → Mirror Pod (API view only means, visible in `kubectl get pods`)
📌 **Every static pod** gets a **mirror pod** automatically created in the API server.

1. Create the Static Pod YAML
```
sudo tee /etc/kubernetes/manifests/mirror-nginx.yaml > /dev/null <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: mirror-nginx
  labels:
    app: mirror-nginx
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - containerPort: 80
EOF
```

2. Verify
```
kubectl get pods -A | grep mirror-nginx
```

3. Optional Cleanup
```
sudo rm /etc/kubernetes/manifests/mirror-nginx.yaml
```

### ⚠️ Notes

- Only works on nodes where `kubelet` is configured with `--pod-manifest-path=/etc/kubernetes/manifests`.
- Mainly used for core components (etcd, kube-apiserver, etc.) in kubeadm setups.