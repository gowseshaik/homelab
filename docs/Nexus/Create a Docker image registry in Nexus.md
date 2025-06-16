Here are the **steps to create a Docker image registry in Nexus** (using Nexus OSS) and allow clients to push/pull using **username/password authentication**.

### ✅ 1. **Install Nexus Repository OSS**

On a server (e.g., `10.14.14.17`):

```bash
docker run -d -p 8081:8081 --name nexus \
  -v nexus-data:/nexus-data \
  sonatype/nexus3
```

Access via: `http://10.14.14.17:8081`

### ✅ 2. **Login & Setup**

- Default credentials:
    - **User**: `admin`
    - **Password**: check with:
        
        ```bash
        docker exec nexus cat /nexus-data/admin.password
        ```
        
- Login → Change password

---

### ✅ 3. **Create a Docker Hosted Registry**

- Go to: **"Repositories"** → **"Create repository"**
- Choose: **docker (hosted)**
    
- Fill:
    - **Name**: `docker-hosted`
    - **HTTP port**: `5007`
    - **Blob store**: (default)
    - Enable **Allow anonymous access** (optional)
        
- Click **Create**

### ✅ 4. **Create a User**

- Go to: **"Security" → "Users"**
- Create a new user (e.g., `dockeruser`)
- Set roles:
    - `nx-repository-view-docker-docker-hosted-*` (read + write)

### ✅ 5. **Allow Docker Client Access (Insecure or Secure)**

#### Option A: **Insecure Registry**

Edit `/etc/containers/registries.conf` (Podman) or `/etc/docker/daemon.json` (Docker):

```json
{
  "insecure-registries": ["10.14.14.17:5007"]
}
```

Then restart:

```bash
sudo systemctl restart docker
# or
sudo systemctl restart podman
```

### ✅ 6. **Login from Client Machine**

```bash
podman login 10.14.14.17:5007
# OR
docker login 10.14.14.17:5007
```

Enter:
- Username: `dockeruser`
- Password: (your created password)

### ✅ 7. **Tag and Push Image**

```bash
podman tag localhost/ubi-unzip:latest 10.14.14.17:5007/cron-image/busybox:latest
podman push 10.14.14.17:5007/cron-image/busybox:latest
```

Let me know if you want to add TLS/SSL or set up proxy/hosted group registries.