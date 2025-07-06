<span style="color:#4caf50;"><b>Created:</b> 2025-06-29</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
## Step 1: Install Filebeat on your localhost (where NGINX runs):
```bash
# Install prerequisite packages
sudo apt-get update && sudo apt-get install -y apt-transport-https wget

# Download and install Elastic GPG key
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

# Add Elastic repo to your sources list (for Ubuntu 24.04 'noble')
echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list

# Update and install filebeat
sudo apt-get update && sudo apt-get install filebeat -y
```

## Step 2: Enable and configure the NGINX module in Filebeat:
```bash
sudo filebeat modules enable nginx
```

## Step 3: Edit Filebeat config file
Edit Filebeat config `/etc/filebeat/filebeat.yml` to point to your ELK (Elasticsearch) inside Multipass:

```
Add or edit output Elasticsearch section:

# vi /etc/filebeat/filebeat.yml

output.elasticsearch:
  hosts: ["<multipass-ip>:9200"]
  username: "elastic"
  password: "<your-elastic-password>"


output.elasticsearch:
  hosts: ["<multipass-ip>:9200"]
  username: "elastic"
  password: "<your-elastic-password>"
```

## Step 4: Set up Filebeat to read NGINX logs 
Set up Filebeat to read NGINX logs (usually `/var/log/nginx/access.log` and `/var/log/nginx/error.log`):

The NGINX module automatically configures this, so no extra manual input is needed if enabled.

5. **Start and enable Filebeat:*
```
gouse@gouse:~/DevOps/multipass_scripts$ sudo filebeat modules
Manage configured modules

Usage:
  filebeat modules [command]

Available Commands:
  disable     Disable one or more given modules
  enable      Enable one or more given modules
  list        List modules


sudo systemctl enable filebeat sudo systemctl start filebeat
```

Note: On ELK (Multipass VM), make sure ports 9200 (Elasticsearch) and 5601 (Kibana) are accessible from your localhost (via port forwarding or firewall rules).

# now enable logs values in nginx inside filebeat dir

cd /etc/filebeat/modules.d
take backup of existing conf `nginx.yml`
vi `nginx.yml'
```
- module: nginx
  access:
    enabled: true
    var.paths: ["/var/log/nginx/access.log"]

  error:
    enabled: true
    var.paths: ["/var/log/nginx/error.log"]

  ingress_controller:
    enabled: false

```

🔄 Then reload and restart Filebeat:
```
sudo filebeat modules enable nginx     # Optional if already done
sudo filebeat setup                    # Optional: sets up dashboards
sudo systemctl restart filebeat
```

### 🧪 To confirm it works:

- Check in Kibana → Discover → `event.module : "nginx"`
- Or check CLI:

```bash
curl -u elastic:admin123 http://localhost:9200/filebeat-*/_search?q=event.module:nginx&pretty
```



```bash
Test the configuration.
sudo filebeat test config
gouse@gouse:/etc/filebeat/modules.d$ sudo filebeat test config
[sudo] password for gouse:
Config OK
```

```bash
Apply Filebeat setup changes.
sudo filebeat setup
```

```bash
gouse@gouse:/etc/filebeat/modules.d$ sudo filebeat setup
Overwriting lifecycle policy is disabled. Set `setup.ilm.overwrite: true` to overwrite.
SDK 2025/06/29 12:32:01 WARN falling back to IMDSv1: operation error ec2imds: getToken, http response error StatusCode: 404, request to EC2 IMDS failed
Index setup finished.
Loading dashboards (Kibana must be running and reachable)
Exiting: error connecting to Kibana: fail to get the Kibana version: HTTP GET request to http://localhost:5601/api/status fails: status=503. Response: {"status":{"overall":{"level":"critical"}}}
```

```

ubuntu@elk-vm:~$ curl http://localhost:5601/api/status
{"status":{"overall":{"level":"unavailable"}}}ubuntu@elk-vm:~$

# update as below vlaues in kibana config
$ sudo vi /etc/kibana/kibana.yml
elasticsearch.hosts: ["https://localhost:9200"]
elasticsearch.ssl.verificationMode: "none"



# resovled the issue by disabling the 
# server.port: 5601

$ sudo systemctl status kibana
$ sudo systemctl start kibana
$ sudo systemctl status kibana --no-page
```

```bash
$ sudo journalctl -u kibana -e

[ERROR][elasticsearch-service] Unable to retrieve version information from Elasticsearch nodes. write EPROTO ...

from:
elasticsearch.hosts: ['https://localhost:9200']
To:
elasticsearch.hosts: ['http://localhost:9200']
sudo systemctl restart kibana

so , now issue resolved:
$ sudo journalctl -u kibana -e
Jun 29 13:42:51 elk-vm systemd[1]: Started Kibana.
....
Jun 29 13:43:12 elk-vm kibana[58924]: [2025-06-29T13:43:12.946+03:00][INFO ][http.server.Preboot] http server running at http://0.0.0.0:5601
Jun 29 13:43:13 elk-vm kibana[58924]: [2025-06-29T13:43:13.349+03:00][INFO ][plugins-system.preboot] Setting up [1] plugins: [interactiveSetup]
```

Able to access dashboard
```
http://100.75.49.6:5601/app/home#/
```


Here's a simple explanation:

## 📄 `filebeat.yml` (Filebeat Configuration File)

- This is the **main configuration file** for **Filebeat**, the log shipping agent.
    
- It tells Filebeat:
    
    - **What files to watch** (log paths)
    - **How to process logs** (parsers, multiline, etc.)
    - **Where to send logs** (Elasticsearch, Logstash, etc.)

### 🧾 Example: `filebeat.yml`

```yaml
filebeat.inputs:
  - type: log
    paths:
      - /var/log/nginx/*.log

output.logstash:
  hosts: ["elk-logstash:5044"]
```

```bash
sudo filebeat test config
sudo systemctl restart filebeat
```

### 🔍 Explanation:

|Section|Purpose|
|---|---|
|`filebeat.inputs`|Defines which files Filebeat reads|
|`type: log`|Says the input is a regular log file|
|`paths`|Log file paths to monitor|
|`output.logstash`|Defines destination (Logstash in this case)|
|`hosts`|IP/hostname of Logstash server|

## 📄 `nginx.conf` or `nginx.yml` (NGINX Config File)

- This config defines how **NGINX** handles HTTP traffic.
    
- Controls:
    
    - Listening ports (e.g., 80/443)
    - Proxy rules
    - SSL certs
    - Load balancing

### 🧾 Example: NGINX Proxy Config

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://127.0.0.1:5601;
    }
}
```

### 🔍 Explanation:

|Section|Purpose|
|---|---|
|`server`|Defines an HTTP listener block|
|`listen 80`|NGINX listens on port 80 (HTTP)|
|`location /`|For all paths (`/`), apply the rule below|
|`proxy_pass`|Forward requests to Kibana on localhost|
## ⚖️ Difference Summary

|Aspect|`filebeat.yml`|`nginx.conf` or `nginx.yml`|
|---|---|---|
|Used by|Filebeat (log shipper)|NGINX (web/proxy server)|
|Purpose|Read and forward logs|Handle and route HTTP traffic|
|Format|YAML|NGINX syntax (not YAML)|
|Key Focus|Log source and destination|Request routing and reverse proxying|

Let me know if you want both configs customized for your ELK setup.