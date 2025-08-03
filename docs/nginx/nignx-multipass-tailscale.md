```json
vi /etc/nginx/sites-available/gitlab

# /etc/nginx/sites-available/argocd.local
server {
    listen 80;
    server_name argocd.local;
    
    location / {
        proxy_pass http://localhost:3000;  # Your service's actual port
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}


http://<multipassip>:8888/
```

Here's a **reverse proxy config** for Nginx to access GitLab running at `http://<multipassip>:8888/`:

### ✅ Nginx Site Config (e.g., `/etc/nginx/sites-available/gitlab`)
- vi /etc/nginx/sites-available/gitlab
```nginx
server {
    listen 80;
    server_name gitlab.local;

    location / {
        proxy_pass http://<multipassip>:8888/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

### ✅ Enable the Config

```bash
sudo ln -s /etc/nginx/sites-available/gitlab /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
Failed to allocate directory watch: Too many open files

gouse@gouse:~$ sudo systemctl stop nginx
Failed to allocate directory watch: Too many open files

so, i killed the pids for nginx and restarted nginx
gouse@gouse:~$ pidof nginx
15682 15537 15536 15535 15533 15532 15531 15530 15529
gouse@gouse:~$ sudo kill -9 15682 15537 15536 15535 15533 15532 15531 15530 15529
gouse@gouse:~$ pidof nginx
gouse@gouse:~$ sudo systemctl restart nginx
```

---

### ✅ Add Domain Mapping on Client

On your **local or remote client** system (not server), add this to `/etc/hosts`:

```text
<your-server-public-ip> gitlab.local
```

Example:

```text
100.120.130.140 gitlab.local
```

---

### ✅ Now Access GitLab

Open browser:

```
http://gitlab.local:8888
```

---

# tailscale ip threw nginx proxy
```Shell
configure in remote host
open /etc/hosts
<tailscaleIP> gitlab.local

and access with http://gitlab.local
```