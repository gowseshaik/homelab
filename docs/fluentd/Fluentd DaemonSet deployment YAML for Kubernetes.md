<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
Here’s a basic **Fluentd DaemonSet deployment YAML** for Kubernetes (output to stdout by default — you can change to Elasticsearch, Loki, etc.):

Actually — ✅ **yes, we did deploy Fluentd** in that YAML.

### Here's how:

- **ConfigMap**: Defines Fluentd's configuration (`fluent.conf`)
    
- **DaemonSet**: Deploys Fluentd on **every node**
    
    - Pulls `fluent/fluentd:v1.14-1` image
        
    - Mounts the logs from host (`/var/log/containers/`)
        
    - Runs using the config from the ConfigMap
        
- **ServiceAccount**: For access control (if needed)


> 🔄 `DaemonSet` ensures **Fluentd runs on each node**, reading logs and processing them as defined.

You can verify deployment with:

```bash
kubectl get pods -n logging -l name=fluentd
```

Let me know if you want a **Loki/Elasticsearch** version or a **Helm chart** method.

```yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: logging

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: logging
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kube.*
      format json
    </source>

    <match **>
      @type stdout
    </match>

---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: logging
  labels:
    k8s-app: fluentd-logging
spec:
  selector:
    matchLabels:
      name: fluentd
  template:
    metadata:
      labels:
        name: fluentd
    spec:
      serviceAccountName: fluentd
      tolerations:
        - key: node-role.kubernetes.io/master
          operator: Exists
          effect: NoSchedule
      containers:
        - name: fluentd
          image: fluent/fluentd:v1.14-1
          env:
            - name: FLUENTD_CONF
              value: fluent.conf
          volumeMounts:
            - name: varlog
              mountPath: /var/log
            - name: config-volume
              mountPath: /fluentd/etc/fluent.conf
              subPath: fluent.conf
      volumes:
        - name: varlog
          hostPath:
            path: /var/log
        - name: config-volume
          configMap:
            name: fluentd-config

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: fluentd
  namespace: logging
```

We can change the output destination (e.g., **Loki**, **Elasticsearch**, **S3**, etc.), so modify the `ConfigMap` section accordingly.

Fluentd itself **does not have a built-in dashboard** for logs or metrics.

### Common practice:

- Fluentd **collects and forwards logs** to logging backends that _do_ provide dashboards, such as:
    
    - **Elasticsearch + Kibana** (Kibana is the dashboard UI)
        
    - **Grafana Loki + Grafana** (Grafana is the dashboard)
        
    - **Splunk**, **Datadog**, **Sumo Logic**, etc.

### Fluentd monitoring:

- You can enable Fluentd metrics (via plugins) and export them to **Prometheus**.
    
- Then visualize Fluentd metrics in **Grafana dashboards** (for Fluentd health, throughput, errors).

### TL;DR:

|Tool|Role|Dashboard|
|---|---|---|
|Fluentd|Log collector and forwarder|No built-in UI|
|Elasticsearch|Log storage and search|Kibana|
|Loki|Log storage|Grafana|
|Prometheus|Metrics collection|Grafana|

If you want, you can set up Fluentd with **Elasticsearch + Kibana** or **Loki + Grafana** for dashboards.