Here's a simple breakdown of **why you need Filebeat and Logstash**, and **when to use which**:

|Tool|Purpose|When to Use|Pros|
|---|---|---|---|
|**Filebeat**|Lightweight log shipper (agent)|On app VMs to **forward logs**|Low CPU/RAM, reliable, easy to use|
|**Logstash**|Centralized log processor & parser|On central VM to **parse/enrich**|Handles complex parsing, filtering|

### 🔹 Why Filebeat?

- Reads logs from files (`/var/log/*.log`, app logs).
- Ships logs to Elasticsearch **or** Logstash.
- Lightweight, low memory usage.
- Ideal for deployment on many machines.

> ✅ Use Filebeat where logs are generated (e.g., app servers, web servers).

### 🔹 Why Logstash?

- Used for **parsing**, **transforming**, and **enriching** logs.
- Can handle complex data (JSON, multiline, grok patterns).
- Used to preprocess logs **before** sending to Elasticsearch.

> ✅ Use Logstash centrally, when logs need parsing before indexing.

### 🔧 Summary Use-Case:

```
[App Server] → Filebeat → [Logstash] → [Elasticsearch] → [Kibana]
```

Or if logs are already clean:

```
[App Server] → Filebeat → [Elasticsearch] → [Kibana]
```

Let me know your use case (plain logs or complex?) and I’ll suggest the best combo.