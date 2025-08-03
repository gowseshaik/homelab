<span style="color:#4caf50;"><b>Created:</b> 2025-08-03</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-08-03</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

Use at least **16+ characters**, random:
```
openssl rand -base64 24
# Example: apm-server.secret_token=Kf84sF9vA4vRzJsP8GzJ+0cR
```
### `docker-compose.yml`

```yaml
version: '3.8'

services:

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.13.4
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - xpack.monitoring.collection.enabled=true
      - bootstrap.memory_lock=true
      - ES_JAVA_OPTS=-Xms1g -Xmx1g
    ulimits:
      memlock:
        soft: -1
        hard: -1
    ports:
      - "9200:9200"
    volumes:
      - esdata:/usr/share/elasticsearch/data

  kibana:
    image: docker.elastic.co/kibana/kibana:8.13.4
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200

  apm-server:
    image: docker.elastic.co/apm/apm-server:8.13.4
    ports:
      - "8200:8200"
    environment:
      - output.elasticsearch.hosts=["http://elasticsearch:9200"]
      - setup.kibana.host=http://kibana:5601
      - apm-server.secret_token=my_secret_token
      - apm-server.host=0.0.0.0:8200
    depends_on:
      - elasticsearch
      - kibana

volumes:
  esdata:
```

---

### 🔧 Commands to run

```bash
docker-compose up -d
```

---

### 📌 After startup

- **Elasticsearch**: [http://localhost:9200](http://localhost:9200)
- **Kibana**: [http://localhost:5601](http://localhost:5601)
- **APM Server**: [http://localhost:8200](http://localhost:8200)

Use `my_secret_token` in your APM agent config.

# Now APM agent configuration to connect APM server

Here are **sample APM agent configurations** for different applications to connect with your Elastic APM Server at `http://localhost:8200` using `admin123` as the secret token:

### ✅ 1. **Java App (Spring Boot / Any JVM)**

Add this to your `JAVA_OPTS` or in systemd/launch script:

```bash
-javaagent:/path/to/elastic-apm-agent.jar \
-Delastic.apm.server_url=http://localhost:8200 \
-Delastic.apm.secret_token=admin123 \
-Delastic.apm.service_name=my-java-app \
-Delastic.apm.environment=dev
```

> 🔗 Download agent: [https://search.maven.org/artifact/co.elastic.apm/elastic-apm-agent](https://search.maven.org/artifact/co.elastic.apm/elastic-apm-agent)

---

### ✅ 2. **Python App (Flask, Django, FastAPI)**

Install agent:

```bash
mkdir flask-apm-app && cd flask-apm-app
python3 -m venv venv
source venv/bin/activate
pip install flask elastic-apm
pip install elastic-apm
```

**Flask Example:**
Create a file `app.py`:
```python
from flask import Flask
from elasticapm.contrib.flask import ElasticAPM

app = Flask(__name__)
app.config['ELASTIC_APM'] = {
  'SERVICE_NAME': 'my-python-app',
  'SECRET_TOKEN': 'admin123',
  'SERVER_URL': 'http://localhost:8200',
  'ENVIRONMENT': 'dev'
}
apm = ElasticAPM(app)



---
from flask import Flask
from elasticapm.contrib.flask import ElasticAPM

app = Flask(__name__)

# APM config
app.config['ELASTIC_APM'] = {
    'SERVICE_NAME': 'my-python-app',
    'SECRET_TOKEN': 'eDSEsZcZeUnj5mFMhrCvOv80BdY5HCAY',  # use your token here
    'SERVER_URL': 'http://localhost:8200',
    'ENVIRONMENT': 'dev'
}

# Enable APM
apm = ElasticAPM(app)

# Sample route
@app.route("/")
def hello():
    return "Hello from Flask + APM!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

```
python app.py
Then visit: http://localhost:5000
```
##### Verify in APM Dashboard
```
Go to http://localhost:5601, then:
- Observability → Services
- You should see `my-python-app` listed.
```

### ✅ 3. **Node.js App (Express, etc.)**

Install agent:

```bash
npm install elastic-apm-node
```

**In your app.js:**

```javascript
require('elastic-apm-node').start({
  serviceName: 'my-node-app',
  secretToken: 'admin123',
  serverUrl: 'http://localhost:8200',
  environment: 'dev'
})
```

---

### ✅ 4. **Go App**

Install:

```bash
go get go.elastic.co/apm
```

**In code:**

```go
import "go.elastic.co/apm/module/apmhttp"

// wrap your handler
http.Handle("/", apmhttp.Wrap(http.HandlerFunc(myHandler)))
```

Set env vars:

```bash
export ELASTIC_APM_SERVER_URL=http://localhost:8200
export ELASTIC_APM_SECRET_TOKEN=admin123
export ELASTIC_APM_SERVICE_NAME=my-go-app
export ELASTIC_APM_ENVIRONMENT=dev
```

---

Let me know which language you're targeting — I can give complete working demo code.