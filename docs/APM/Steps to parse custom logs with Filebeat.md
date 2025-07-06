<span style="color:#4caf50;"><b>Created:</b> 2025-06-29</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

For **custom logs**, you don’t use a module — instead, you configure a **custom Filebeat input** and optionally use **Elasticsearch ingest pipelines** to parse the logs.

### ✅ Steps to parse custom logs with Filebeat:

1. **Edit Filebeat config:**

```bash
sudo vi /etc/filebeat/filebeat.yml


# ======================= Filebeat inputs ===============================

filebeat.inputs:

# Each - is an input. Most options can be set at the input level, so
# you can use different inputs for various configurations.
# Below are the input-specific configurations.

# filestream is an input for collecting log messages from files.
- type: filestream

  # Unique ID among all inputs, an ID is required.
  id: my-filestream-id

  # Change to true to enable this input configuration.
  enabled: false

  # Paths that should be crawled and fetched. Glob based paths.
  paths:
    - /var/log/*.log


# ---------------------------- Elasticsearch Output ----------------------------
output.elasticsearch:
  # Array of hosts to connect to.
  hosts: ["http://localhost:9200"]

  # Performance preset - one of "balanced", "throughput", "scale",
  # "latency", or "custom".
  preset: balanced

  # Protocol - either `http` (default) or `https`.
  #protocol: "https"

  # Authentication credentials - either API key or username/password.
  #api_key: "id:api_key"
  username: "elastic"
  password: "admin123"

```

2. **Add a custom input:**

```yaml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/myapp/*.log    # Change to your log path
    fields:
      log_type: custom          # Optional tag
    multiline.pattern: '^\['    # If logs span multiple lines, example: starts with [
    multiline.negate: true
    multiline.match: after
```

3. **(Optional) Define parsing via Elasticsearch pipeline or Logstash (if used)**

If logs are in custom format, you can create a pipeline in Elasticsearch and apply it using:

```yaml
output.elasticsearch:
  hosts: ["http://<elk-ip>:9200"]
  pipeline: "my-custom-pipeline"
```

### 🔍 Optional: Test config and start filebeat

```bash
sudo filebeat test config
sudo systemctl restart filebeat
```

Let me know if you want help writing a custom **grok pattern** or **pipeline** for your log format (just paste a few sample log lines).
