

When you need to expose multiple services through the same ports (80 for HTTP or 443 for HTTPS), you'll use **name-based virtual hosting** in Nginx. Here's how to set this up properly:

## Solution: Name-Based Virtual Hosting

All services will share ports 80/443, with Nginx routing traffic based on the hostname.

### 1. Base Configuration Structure

Create separate files in `/etc/nginx/sites-available/` for each service:

```bash
sudo nano /etc/nginx/sites-available/service1.example.com
sudo nano /etc/nginx/sites-available/service2.example.com

sudo vi /etc/nginx/sites-available/argocd.local
```

### 2. Sample Configurations

**For HTTP (port 80):**
```nginx
# /etc/nginx/sites-available/service1.example.com
server {
    listen 80;
    server_name service1.example.com;
    
    location / {
        proxy_pass http://localhost:3000;  # Your service's actual port
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}



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
```

**For HTTPS (port 443):**
```nginx
# /etc/nginx/sites-available/service2.example.com
server {
    listen 443 ssl;
    server_name service2.example.com;
    
    ssl_certificate /etc/ssl/certs/service2.pem;
    ssl_certificate_key /etc/ssl/private/service2.key;
    
    location / {
        proxy_pass http://localhost:4000;  # Your service's actual port
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

### 3. Enable the Configurations

```bash
sudo ln -s /etc/nginx/sites-available/service1.example.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/service2.example.com /etc/nginx/sites-enabled/


sudo ln -s /etc/nginx/sites-available/argocd.local /etc/nginx/sites-enabled/
```

### 4. Default Server Handling

Add a default catch-all server to handle unmatched requests:

```bash
sudo nano /etc/nginx/sites-available/default
```

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    return 444;  # Close connection silently
}

server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;
    server_name _;
    ssl_certificate /etc/ssl/certs/default.pem;
    ssl_certificate_key /etc/ssl/private/default.key;
    return 444;
}
```

## Tailscale-Specific Configuration

For Tailscale access, you have two options:

### Option A: Use Tailscale MagicDNS
```nginx
server {
    listen 80;
    server_name service1.your-tailnet-name.ts.net;
    # ... rest of config
}
```

### Option B: Use Tailscale IP with Host Header
```nginx
server {
    listen 80;
    server_name 100.xx.yy.zz;  # Your Tailscale IP
    
    location /service1 {
        proxy_pass http://localhost:3000;
        # ... headers
    }
    
    location /service2 {
        proxy_pass http://localhost:4000;
        # ... headers
    }
}
```

## Verification and Maintenance

1. **Test your configuration**:
   ```bash
   sudo nginx -t
   ```

2. **Reload Nginx**:
   ```bash
   sudo systemctl reload nginx
   ```

3. **Check active connections**:
   ```bash
   sudo tail -f /var/log/nginx/access.log
   ```

4. **Add new services**:
   - Create new config file in `/etc/nginx/sites-available/`
   - Link to `/etc/nginx/sites-enabled/`
   - Reload Nginx

## Important Notes

1. All hostnames must resolve to your server's IP (via DNS or Tailscale MagicDNS)
2. For HTTPS, you'll need certificates for each hostname
3. Consider using a wildcard certificate if you have many subdomains
4. Tailscale can automatically provision certificates for `*.ts.net` domains
