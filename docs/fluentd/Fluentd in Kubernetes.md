<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

|**W3H**|**Details**|
|---|---|
|**What**|Fluentd is a log collector and forwarder that unifies logging across systems.|
|**Why**|To collect, process, filter, and send logs from containers to destinations like Elasticsearch, Loki, S3, etc.|
|**Where**|Runs as a **DaemonSet** on each Kubernetes node to access container logs via `/var/log/containers/` or CRI socket.|
|**How**|Deploy Fluentd as a DaemonSet + ConfigMap for parsing + output plugin for destination. Example: Fluentd → Elasticsearch or Fluentd → Loki.|
