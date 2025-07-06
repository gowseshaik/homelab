<span style="color:#4caf50;"><b>Created:</b> 2025-06-29</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

### Best Practice Setup (4 VMs):

1. `elk-es` – 4 CPU, 4–8 GB RAM, 20+ GB Disk
2. `elk-kibana` – 2 CPU, 2 GB RAM
3. `elk-logstash` – 2–4 CPU, 4 GB RAM
4. `elk-agent-app1` – Filebeat (with your app) – 1 CPU, 1 GB RAM

### 🔧 Step 1: Create VMs with resources

```bash
# Create Elasticsearch VM
multipass launch --name elk-es --cpus 4 --mem 8G --disk 20G

# Create Kibana VM
multipass launch --name elk-kibana --cpus 2 --mem 2G --disk 10G

# Create Logstash VM
multipass launch --name elk-logstash --cpus 4 --mem 4G --disk 15G

# Create Filebeat Agent VM (can simulate app logs)
multipass launch --name elk-agent-app1 --cpus 1 --mem 1G --disk 5G
```
### 🔧 Step 2: Install Elasticsearch on `elk-es`

```bash
multipass exec elk-es -- bash -c '
sudo apt update
sudo apt install -y wget apt-transport-https openjdk-17-jdk
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
sudo apt update
sudo apt install -y elasticsearch
sudo systemctl enable elasticsearch
sudo systemctl start elasticsearch
'
```
### 🔧 Step 3: Install Kibana on `elk-kibana`

```bash
multipass exec elk-kibana -- bash -c '
sudo apt update
sudo apt install -y wget apt-transport-https openjdk-17-jdk
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
sudo apt update
sudo apt install -y kibana
sudo systemctl enable kibana
sudo systemctl start kibana
'
```
### 🔧 Step 4: Install Logstash on `elk-logstash`

```bash
multipass exec elk-logstash -- bash -c '
sudo apt update
sudo apt install -y wget apt-transport-https openjdk-17-jdk
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
sudo apt update
sudo apt install -y logstash
sudo systemctl enable logstash
sudo systemctl start logstash
'
```
### 🔧 Step 5: Install Filebeat on `elk-agent-app1`

```bash
multipass exec elk-agent-app1 -- bash -c '
sudo apt update
sudo apt install -y wget apt-transport-https
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
sudo apt update
sudo apt install -y filebeat
sudo systemctl enable filebeat
sudo systemctl start filebeat
'
```
### ✅ Result

|VM Name|Component|Status|
|---|---|---|
|`elk-es`|Elasticsearch|✅ Installed|
|`elk-kibana`|Kibana|✅ Installed|
|`elk-logstash`|Logstash|✅ Installed|
|`elk-agent-app1`|Filebeat|✅ Installed|

Let me know if you want config files for `logstash`, `filebeat`, or port forwarding/Nginx setup.

# Below is the single automated Bash script to:

✅ Create 4 VMs using Multipass  
✅ Install Elasticsearch, Kibana, Logstash, Filebeat  
✅ Set required resources for each  
✅ Enable and start all services

### ✅ `setup-elk.sh`

```
#!/bin/bash

# Create VMs
echo "Creating VMs..."
multipass launch --name elk-es --cpus 4 --mem 8G --disk 20G
multipass launch --name elk-kibana --cpus 2 --mem 2G --disk 10G
multipass launch --name elk-logstash --cpus 4 --mem 4G --disk 15G
multipass launch --name elk-agent-app1 --cpus 1 --mem 1G --disk 5G

# Common Elastic APT setup
APT_SETUP=$(cat <<'EOF'
sudo apt update
sudo apt install -y wget apt-transport-https gnupg openjdk-17-jdk
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
sudo apt update
EOF
)

# Install Elasticsearch
echo "Installing Elasticsearch on elk-es..."
multipass exec elk-es -- bash -c "$APT_SETUP && sudo apt install -y elasticsearch && sudo systemctl enable --now elasticsearch"

# Install Kibana
echo "Installing Kibana on elk-kibana..."
multipass exec elk-kibana -- bash -c "$APT_SETUP && sudo apt install -y kibana && sudo systemctl enable --now kibana"

# Install Logstash
echo "Installing Logstash on elk-logstash..."
multipass exec elk-logstash -- bash -c "$APT_SETUP && sudo apt install -y logstash && sudo systemctl enable --now logstash"

# Install Filebeat
echo "Installing Filebeat on elk-agent-app1..."
multipass exec elk-agent-app1 -- bash -c "$APT_SETUP && sudo apt install -y filebeat && sudo systemctl enable --now filebeat"

echo -e "\n✅ ELK Stack setup completed on Multipass VMs!"
multipass list
```

---

### 📌 Usage

1. Save as `setup-elk.sh`
2. Run:

```bash
chmod +x setup-elk.sh
./setup-elk.sh
```

Let me know if you want:

- Config files (`filebeat.yml`, `logstash.conf`)
- External access via port forwarding or Nginx
- Sample logs to ingest

# nginx to configure
```
sudo nginx -t && sudo systemctl reload nginx
```