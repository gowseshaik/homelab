Here are the steps to install and configure Fluentd on a standalone Linux VM to collect and forward logs (e.g., Siebel logs):
### 1. **Install Fluentd**
```bash
# Install td-agent (Fluentd stable distribution) on Ubuntu/Debian:
curl -fsSL https://packages.treasuredata.com/GPG-KEY-td-agent | sudo apt-key add -
echo "deb https://packages.treasuredata.com/4/ubuntu/$(lsb_release -cs)/ $(lsb_release -cs) contrib" | sudo tee /etc/apt/sources.list.d/treasure-data.list
sudo apt-get update
sudo apt-get install -y td-agent
```
### 2. **Configure Fluentd**
Edit the main config file `/etc/td-agent/td-agent.conf`:
Example to tail Siebel logs (adjust `/path/to/siebel/logs/*.log`):

```conf
<source>
  @type tail
  path /path/to/siebel/logs/*.log
  pos_file /var/log/td-agent/siebel.log.pos
  tag siebel.logs
  format none
</source>

<match siebel.logs>
  @type stdout
  # For forwarding to Elasticsearch, replace above with:
  # @type elasticsearch
  # host localhost
  # port 9200
</match>
```
### 3. **Restart Fluentd**
```bash
sudo systemctl restart td-agent
sudo systemctl enable td-agent
```
### 4. **Verify Fluentd is running**
```bash
sudo systemctl status td-agent
tail -f /var/log/td-agent/td-agent.log
```

### Optional: Forward logs to Elasticsearch or other destinations

Replace the `<match>` block with appropriate output plugin config, for example:

```conf
<match siebel.logs>
  @type elasticsearch
  host your-elasticsearch-host
  port 9200
  logstash_format true
  index_name siebel-logs
</match>
```
