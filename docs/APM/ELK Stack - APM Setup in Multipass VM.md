I'll help you set up Elasticsearch, Kibana, and APM Server in a Multipass VM. This is a comprehensive setup that requires several steps.This guide will help you set up a complete ELK stack with APM monitoring in a Multipass VM. Here are some key points to keep in mind:

**Resource Requirements:**

- The VM is configured with 4 CPUs, 8GB RAM, and 20GB disk space, which should be sufficient for development
- Elasticsearch uses 2GB of heap memory by default - adjust if needed

**Important Notes:**

1. **Security is disabled** in this setup for easier development - enable it for production use
2. **Single-node configuration** - suitable for development but not for production clusters
3. **Network access** is configured to allow connections from your host machine

**Quick Start Sequence:**

1. Create the VM and SSH into it
2. Run the installation commands in order
3. Wait for all services to start (Elasticsearch takes the longest)
4. Access Kibana at `http://VM_IP:5601` to verify everything is working

**Common Issues:**

- If services fail to start, check the logs using the journalctl commands provided
- Memory issues can be resolved by increasing VM memory or reducing JVM heap size
- Network connectivity issues usually resolve by using the correct VM IP address

## Step 1: Create and Configure Multipass VM

```bash
# Create a VM with sufficient resources
multipass launch --name elk-stack --cpus 4 --memory 8G --disk 20G

# Get shell access
multipass shell elk-stack
```

## Step 2: Update System and Install Prerequisites

```bash
# Update package list
sudo apt update && sudo apt upgrade -y

# Install Java (required for Elasticsearch)
sudo apt install openjdk-11-jdk -y

# Verify Java installation
java -version

# Install curl, wget, and gnupg
sudo apt install curl wget gnupg2 -y
```

## Step 3: Add Elastic Repository

```bash
# Import Elastic GPG key
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg

# Add Elastic repository
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list

# Update package list
sudo apt update
```

## Step 4: Install Elasticsearch

```bash
# Install Elasticsearch
sudo apt install elasticsearch -y

# Configure Elasticsearch
sudo vi /etc/elasticsearch/elasticsearch.yml
```

### Elasticsearch Configuration (`/etc/elasticsearch/elasticsearch.yml`)

```yaml
# Cluster name
cluster.name: my-application

# Node name
node.name: node-1

# Network settings
network.host: 0.0.0.0
http.port: 9200

# Discovery settings for single node
discovery.type: single-node

# Security settings (disable for development)
xpack.security.enabled: false
xpack.security.enrollment.enabled: false
xpack.security.http.ssl.enabled: false
xpack.security.transport.ssl.enabled: false

# Memory settings
bootstrap.memory_lock: true
```

### Configure JVM Heap Size

```bash
# Edit JVM options
sudo vi /etc/elasticsearch/jvm.options.d/heap.options
```

Add the following content:

```
-Xms2g
-Xmx2g
```

### Start Elasticsearch

```bash
# Enable and start Elasticsearch
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch
sudo systemctl start elasticsearch

# Check status
sudo systemctl status elasticsearch

# Test Elasticsearch
curl -X GET "localhost:9200/"
```

## Step 5: Install Kibana

```bash
# Install Kibana
sudo apt install kibana -y

# Configure Kibana
sudo nano /etc/kibana/kibana.yml
```

### Kibana Configuration (`/etc/kibana/kibana.yml`)

```yaml
# Server settings
server.port: 5601
server.host: "0.0.0.0"
server.name: "kibana-server"

# Elasticsearch settings
elasticsearch.hosts: ["http://localhost:9200"]

# Disable security for development
xpack.security.enabled: false
xpack.encryptedSavedObjects.encryptionKey: "something_at_least_32_characters_long"
```

### Start Kibana

```bash
# Enable and start Kibana
sudo systemctl enable kibana
sudo systemctl start kibana

# Check status
sudo systemctl status kibana
```

## Step 6: Install APM Server

```bash
# Install APM Server
sudo apt install apm-server -y

# Configure APM Server
sudo nano /etc/apm-server/apm-server.yml
```

### APM Server Configuration (`/etc/apm-server/apm-server.yml`)

```yaml
# APM Server settings
apm-server:
  host: "0.0.0.0:8200"
  rum:
    enabled: true
    allow_origins: ['*']

# Output to Elasticsearch
output.elasticsearch:
  hosts: ["localhost:9200"]
  
# Kibana settings
setup.kibana:
  host: "localhost:5601"
  
# Disable security
apm-server.auth.anonymous.enabled: true
```

### Setup APM Server

```bash
# Setup APM Server dashboards and templates
sudo apm-server setup -e

# Enable and start APM Server
sudo systemctl enable apm-server
sudo systemctl start apm-server

# Check status
sudo systemctl status apm-server
```

## Step 7: Configure VM Network Access

```bash
# Get VM IP address
ip addr show

# Note the IP address (usually 192.168.x.x)
```

From your host machine:

```bash
# Get VM info
multipass info elk-stack

# The VM IP will be shown - use this to access services
```

## Step 8: Access Services

Open your web browser and navigate to:

- **Kibana**: `http://VM_IP:5601`
- **Elasticsearch**: `http://VM_IP:9200`
- **APM Server**: `http://VM_IP:8200` (for agent connections)

## Step 9: Verify Installation

### Test Elasticsearch

```bash
curl -X GET "VM_IP:9200/_cluster/health?pretty"
```

### Test APM Server

```bash
curl -X GET "VM_IP:8200/"
```

### Access Kibana

1. Open `http://VM_IP:5601` in your browser
2. Go to "APM" section to verify APM integration
3. Check "Stack Management" > "Index Management" for APM indices

## Step 10: Basic APM Usage

### Install APM Agent (Example for Node.js)

```bash
# In your application directory
npm install elastic-apm-node --save
```

### Configure APM Agent

```javascript
// At the top of your main application file
const apm = require('elastic-apm-node').start({
  serviceName: 'my-service',
  serverUrl: 'http://VM_IP:8200',
  environment: 'development'
})
```

## Troubleshooting

### Check Logs

```bash
# Elasticsearch logs
sudo journalctl -u elasticsearch -f

# Kibana logs
sudo journalctl -u kibana -f

# APM Server logs
sudo journalctl -u apm-server -f
```

### Restart Services

```bash
sudo systemctl restart elasticsearch
sudo systemctl restart kibana
sudo systemctl restart apm-server
```

### Memory Issues

If you encounter memory issues, you can:

1. Increase VM memory: `multipass set local.elk-stack.memory=12G`
2. Reduce JVM heap size in `/etc/elasticsearch/jvm.options.d/heap.options`

## Security Note

This setup disables security features for development purposes. For production use, enable security features and configure proper authentication and encryption.

## Port Summary

- **Elasticsearch**: 9200
- **Kibana**: 5601
- **APM Server**: 8200

Make sure these ports are accessible from your host machine to the VM.

