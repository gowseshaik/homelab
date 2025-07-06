<span style="color:#4caf50;"><b>Created:</b> 2025-06-29</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
```bash
sudo apt update
sudo apt install ufw
If UFW is showing as "inactive," you need to enable it before allowing any ports. Follow these steps:
sudo ufw status
sudo ufw enable

sudo ufw allow 3389/tcp
sudo ufw allow 8080/tcp
sudo ufw allow 80/tcp
sudo ufw allow 4000/tcp
sudo ufw allow 5601/tcp # for kibana
sudo ufw allow 9200 # for elasticsearch

If you don't want to use UFW and prefer using `iptables`, you can allow the port with:

sudo iptables -A INPUT -p tcp --dport 3389 -j ACCEPT

Don't forget to save the `iptables` rules to make sure they persist after a reboot:

sudo apt install iptables-persistent
sudo netfilter-persistent save
```
## Now port forwarding to Multipass VMs with nginx
Yes — if you don’t want to use `socat` with `nohup`, here are **cleaner and better alternatives** to forward port 5601 to `localhost`:

## ✅ Option 1: Use `systemd` service for socat (cleaner than `nohup`)

### 🔧 Create systemd service on host:
```bash
sudo tee /etc/systemd/system/socat-kibana.service > /dev/null <<EOF
[Unit]
Description=Port forward Kibana from Multipass VM to localhost:5601
After=network.target

[Service]
ExecStart=/usr/bin/socat TCP-LISTEN:5601,fork TCP:$(multipass info elk-vm | grep IPv4 | awk '{print $2}'):5601
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

```bash
# Enable and start
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable --now socat-kibana.service
```

> Now, Kibana is always available at `localhost:5601` and runs cleanly as a background service.

## ✅ Option 2: Use `nginx` reverse proxy on host (No socat)

1. **Install nginx on host:**
```bash
sudo apt install nginx
```

2. **Create reverse proxy config:**
```bash
sudo tee /etc/nginx/sites-available/kibana > /dev/null <<EOF
server {
    listen 5601;
    location / {
        proxy_pass http://$(multipass info elk-vm | grep IPv4 | awk '{print $2}'):5601;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF
```

```bash
sudo tee /etc/nginx/sites-available/elasticsearch > /dev/null <<EOF
server {
    listen 9200;
    location / {
        proxy_pass http://192.168.64.5:9200;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF
```

3. **Enable site and reload nginx:**
```bash
sudo ln -s /etc/nginx/sites-available/kibana /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/elasticsearch /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

> ✅ Now open `http://localhost:5601` — it will reverse proxy to the Kibana inside the VM.

## ✅ Recommendation

|Method|Use Case|Notes|
|---|---|---|
|`systemd + socat`|You want clean auto-starting service|Better than `nohup`|
|`nginx`|You prefer proxy and load balancing|No `socat` needed|
|`ssh -L`|You want temporary port tunnel|Manual each time|

Let me know which one you want to keep — I can give cleanup steps for the others.
###  Port foward with socat

### ✅ Basic Port Forward: Host → VM (Kibana)
```bash
sudo socat TCP-LISTEN:5601,fork TCP:<vm-ip>:5601
```

> Forwards **localhost:5601** on host to `elk-vm:5601`

### ⏳ Run in background (useful for long running)
```bash
sudo nohup socat TCP-LISTEN:5601,fork TCP:<vm-ip>:5601 &
```

> Runs `socat` in background using `nohup`

### 🧼 Kill existing socat port forward (if stuck)
```bash
sudo pkill -f "socat.*5601"
```

> Stops any `socat` process handling port 5601

### 🧪 Test port forward locally
```bash
curl http://localhost:5601
```

> This will now hit the VM's Kibana

### 📝 Replace `<vm-ip>` using command:
```bash
multipass info elk-vm | grep IPv4 | awk '{print $2}'
```

