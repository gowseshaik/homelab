<span style="color:#4caf50;"><b>Created:</b> 2025-08-03</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-08-03</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

You can use **any free port** — not just 8080. 8080 is simply a **common convention** for web apps when port 80 is taken or reserved.
### ✅ Why 8080 is Common:

|Port|Usage|
|---|---|
|80|Default HTTP (already used by Apache2 or Nginx)|
|443|Default HTTPS|
|8080|Common alternative for HTTP (easy to remember)|
|8888|Also used often for apps (like Jupyter, test servers)|
|3000|Common for dev servers (Node.js, React, etc.)|
|9090|Often used by monitoring tools (e.g., Prometheus)|

### ✅ So you can pick:

- `8081`, `8082`, `8888`, `3001`, `5000`, etc.
- Just make sure the port is:
    - **Not used** (`sudo lsof -i :<port>`)
    - **Allowed by firewall** (`sudo ufw allow <port>`)

---

### 🔄 Example

You want GitLab on port **8888**:

1. In `/etc/gitlab/gitlab.rb`:
```ruby
external_url 'http://100.189.165.169:8888'
```
    
2. Then:
```bash
sudo gitlab-ctl reconfigure
sudo gitlab-ctl restart
sudo lsof -i :8888
sudo ufw allow 8888
```

```Shell
buntu@gitlab-ce:~$ sudo lsof -i :8888
COMMAND     PID       USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
gitlab-ka 37234        git    6u  IPv4 196486      0t0  TCP gitlab-ce.multipass:52078->gitlab-ce.multipass:8888 (ESTABLISHED)
nginx     37245       root    7u  IPv4 197636      0t0  TCP *:8888 (LISTEN)
nginx     37246 gitlab-www    3u  IPv4 196808      0t0  TCP gitlab-ce.multipass:8888->gitlab-ce.multipass:52078 (ESTABLISHED)
nginx     37246 gitlab-www    7u  IPv4 197636      0t0  TCP *:8888 (LISTEN)
nginx     37247 gitlab-www    7u  IPv4 197636      0t0  TCP *:8888 (LISTEN)
nginx     37248 gitlab-www    7u  IPv4 197636      0t0  TCP *:8888 (LISTEN)
nginx     37249 gitlab-www    7u  IPv4 197636      0t0  TCP *:8888 (LISTEN)

ubuntu@gitlab-ce:~$ sudo lsof -i :9090
COMMAND     PID              USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
prometheu 36090 gitlab-prometheus    6u  IPv4 184641      0t0  TCP localhost:9090 (LISTEN)
prometheu 36090 gitlab-prometheus   23u  IPv4 184209      0t0  TCP localhost:42624->localhost:9090 (ESTABLISHED)
prometheu 36090 gitlab-prometheus   24u  IPv4 184210      0t0  TCP localhost:9090->localhost:42624 (ESTABLISHED)
ubuntu@gitlab-ce:~$ sudo lsof -i :80
ubuntu@gitlab-ce:~$ 
```
   
3. Access:
```bash
curl http://100.189.165.169:8888
```


Use whatever port works for you — just avoid conflicts with existing services.