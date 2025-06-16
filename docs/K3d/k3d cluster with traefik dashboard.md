To enable and expose the **Traefik dashboard** in `k3d` at cluster creation, you need to do **two things** in the config file:

---

### ✅ 1. Enable Traefik Dashboard via k3s Arg

Add this under the `k3s` section:

```yaml
k3s:
  extraArgs:
    - arg: "--traefik.dashboard=true"
      nodeFilters:
        - server:*
```

---

### ✅ 2. Expose Traefik Dashboard Port (default is 9000)

Add this under the `ports:` section:

```yaml
  - port: 30900:9000      # Traefik Dashboard
    nodeFilters:
      - loadbalancer
```

---

### ✅ ✅ Final Config: `k3d-config.yaml`

```
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
  - port: 30099:3000     # Grafana (optional)
    nodeFilters:
      - loadbalancer
  - port: 30900:9000     # Traefik Dashboard
    nodeFilters:
      - loadbalancer
k3s:                      # not working for k3s version, so you can remove it.
  extraArgs:
    - arg: "--traefik.dashboard=true"
      nodeFilters:
        - server:*
```

---

but it getting below error for k3s 
```bash
 k3d cluster create --config dev-cluster.yaml
FATA[0000] Schema Validation failed for config file dev-cluster.yaml: - (root): Additional property k3s is not allowed
```

You're seeing the error because `k3d v5+` **no longer supports** the `k3s:` block in the config file.  
That field is **not valid** in the latest schema (v1alpha5).

---

### ✅ **Solution: Use `--k3s-arg` from CLI instead**

Yes, exactly.

Remove the entire `k3s:` section from your config file.

Use only the cluster definition and port mappings in the YAML, then pass k3s arguments like `--traefik.dashboard=true` via the CLI when creating the cluster.

Since the config file doesn't support `k3s:` anymore, you can enable the Traefik dashboard like this:

```bash
k3d cluster create --config dev-cluster.yaml \
  --k3s-arg "--traefik.dashboard=true@server:0"
```

This passes the arg `--traefik.dashboard=true` to the first server node.

---

### ✅ Optional: Alias for Simplicity

If you want to reuse this, put it in a shell script:

```bash
#!/bin/bash
k3d cluster create --config dev-cluster.yaml \
  --k3s-arg "--traefik.dashboard=true@server:*"
```

---

Let me know if you want a workaround to fully control the k3s startup args from config (e.g., custom entrypoint container).

## why can't we use these values in config file ?
Great question — here’s a straight answer:

---

### 🔴 **Why you can't use `k3s:` in `k3d` config anymore**

- In **`k3d v5+`**, the config file follows a **strict JSON schema** (`v1alpha5`) that **does not include** a `k3s:` field.
    
- The field was **removed** to simplify the config format and separate cluster structure (YAML) from runtime behavior (CLI flags).
    
- So, `k3s:` and `extraArgs` were **deprecated** and **replaced** by `--k3s-arg` flags in the CLI only.
    

---

### ✅ Current Rule:

- Cluster topology (nodes, ports, volumes, registries) → ✅ defined in YAML.
    
- Runtime args (like `--traefik.*`, `--disable-*`, `--tls-san`, etc.) → ❌ not in YAML → ✅ only via CLI `--k3s-arg`.
    

---

### 🔄 Legacy Compatibility?

No official backward support. Even if you add `k3s:` in the YAML, `k3d` will **fail schema validation**.

---

Let me know if you want to build a wrapper that merges YAML + CLI for easier reuse.
### 🌐 Access Traefik Dashboard:

After cluster creation:

```
http://localhost:30900/dashboard/
```

Let me know if you want to secure it or route it via Ingress host like `traefik.localhost`.

If your cluster creation **hangs on starting the server**, here are the most common and effective fixes:

---

### ✅ **1. Check for Docker Conflicts**

Run this to see if containers are stuck or conflicting:

```bash
docker ps -a | grep k3d
```

If any containers are in a `Created` or `Exited` state, clean them:

```bash
k3d cluster delete dev-cluster
docker system prune -f
```

Then try again.

---

### ✅ **2. Make Sure Ports Aren’t Already in Use**

You’re mapping ports like `31446`, `31447`, etc.  
Run:

```bash
lsof -i -P -n | grep LISTEN
```

Look for conflicting ports. If a port is in use, either:

- Stop the app using it, or
    
- Change the port in `dev-cluster.yaml`
    

---

### ✅ **3. Disable Traefik Temporarily**

Test if the arg is causing the issue by removing it:

```bash
k3d cluster create --config dev-cluster.yaml
```

If that works, try:

```bash
k3d cluster create --config dev-cluster.yaml --k3s-arg "--disable=traefik@server:0"
```

Then install your own ingress later (e.g., Traefik/NGINX manually).

---

### ✅ **4. Increase Docker Memory**

If your Docker is low on memory (common with 2+ agents), bump it up in Docker Desktop:

> Settings → Resources → Memory → Increase to at least **4–6 GB**

---

### ✅ **5. Check Logs**

If it still hangs, grab logs from the server node:

```bash
docker logs k3d-dev-cluster-server-0
```

Paste the output here if you'd like me to help debug further.

Thanks — this confirms it clearly:

> **Port 9000 is mapped**, but **nothing is listening on it inside the cluster.**  
> → That means the **Traefik dashboard is not enabled** in your k3s setup.

---

### ✅ Fix: Recreate Cluster with Dashboard Enabled

You need to add this flag during cluster creation:

```bash
--k3s-arg "--traefik.dashboard=true@server:0"
```

So update your `k3d` create command like:

```bash
k3d cluster delete dev-cluster

k3d cluster create --config dev-cluster.yaml \
  --k3s-arg "--traefik.dashboard=true@server:0"
```

Make sure this is already in your `dev-cluster.yaml`:

```yaml
- port: 30900:9000
  nodeFilters:
    - loadbalancer
```

---

### 🔍 Optional: Also expose dashboard via ingress (cleaner)

You can create an ingress like this (after cluster up):

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: traefik-dashboard
  namespace: kube-system
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: web
    traefik.ingress.kubernetes.io/router.middlewares: kube-system-auth@kubernetescrd
spec:
  rules:
    - host: traefik.localhost
      http:
        paths:
          - path: /dashboard/
            pathType: Prefix
            backend:
              service:
                name: traefik
                port:
                  number: 9000
```

Then access:

```
http://traefik.localhost/dashboard/
```

(using a `hosts` file entry if needed)

---

Let me know once you recreate the cluster with the dashboard flag — you should be able to access:

```
http://localhost:30900/dashboard/
```

To access `http://traefik.localhost/dashboard/` from your browser, you need to map the custom domain `traefik.localhost` to your local machine.

---

### ✅ Steps to Add Entry in `/etc/hosts`

1. Open the `/etc/hosts` file with root privileges:
    
    ```bash
    sudo nano /etc/hosts
    ```
    
2. Add this line at the end of the file:
    
    ```
    127.0.0.1 traefik.localhost
    ```
    
3. Save and exit:
    
    - Press `Ctrl + O` to save
        
    - Press `Enter` to confirm
        
    - Press `Ctrl + X` to exit
        

---

### 📌 After That

Make sure:

- You’ve created an **Ingress** with `host: traefik.localhost`
    
- Traefik is listening on port 80 (mapped via `30080:80@loadbalancer`)
    

Then access:

```
http://traefik.localhost:30080/dashboard/
```

> (or just `http://traefik.localhost/dashboard/` if port 80 is directly forwarded)

Let me know if you want the ingress YAML again.