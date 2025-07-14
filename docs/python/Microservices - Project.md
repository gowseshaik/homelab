## 📁 1. Project Structure Creation

```bash
mkdir -p scraper-microservices/{scraper-service/app/{routes,scrapers,models},shared,k8s/{scraper,kong,redis}}
cd scraper-microservices
touch scraper-service/{Dockerfile,requirements.txt}
touch scraper-service/app/main.py
```

---

## ⚙️ 2. Setup Python Scraper Microservice (FastAPI)

**scraper-service/requirements.txt**

```
fastapi
uvicorn
requests
beautifulsoup4
```

**scraper-service/app/main.py**

```python
from fastapi import FastAPI
from app.routes import scrape

app = FastAPI()
app.include_router(scrape.router)
```

**scraper-service/app/routes/scrape.py**

```python
from fastapi import APIRouter, Query
from app.scrapers import amazon, noon

router = APIRouter()

@router.get("/scrape")
def scrape(site: str = Query(...), q: str = Query(...)):
    if site == "amazon":
        return amazon.scrape(q)
    elif site == "noon":
        return noon.scrape(q)
    return {"error": "unsupported site"}
```

**scraper-service/app/scrapers/amazon.py**

```python
def scrape(query):
    return {"site": "amazon", "query": query}
```

**scraper-service/app/scrapers/noon.py**

```python
def scrape(query):
    return {"site": "noon", "query": query}
```

---

## 🐳 3. Add Dockerfile

**scraper-service/Dockerfile**

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🧪 4. Add Docker Compose for Local Testing

**docker-compose.yml**

```yaml
version: '3'
services:
  scraper:
    build: ./scraper-service
    ports:
      - "8000:8000"
  redis:
    image: redis:7
```

---

## ☸️ 5. Add Kubernetes YAMLs

**k8s/scraper/deployment.yaml**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: scraper
spec:
  replicas: 1
  selector:
    matchLabels:
      app: scraper
  template:
    metadata:
      labels:
        app: scraper
    spec:
      containers:
        - name: scraper
          image: ttl.sh/scraper:1h
          ports:
            - containerPort: 8000
```

**k8s/scraper/service.yaml**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: scraper-service
spec:
  selector:
    app: scraper
  ports:
    - port: 8000
      targetPort: 8000
```

---

## 🌐 6. Kong Gateway Setup (Ingress)

**k8s/kong/scraper-ingress.yaml**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: scraper-ingress
  annotations:
    konghq.com/strip-path: "true"
spec:
  rules:
    - http:
        paths:
          - path: /scraper
            pathType: Prefix
            backend:
              service:
                name: scraper-service
                port:
                  number: 8000
```

---

## 📦 7. Build & Push Image to `ttl.sh`

```bash
docker build -t ttl.sh/scraper:1h ./scraper-service
docker push ttl.sh/scraper:1h
```

---

Would you like the Helm install steps for Kong Gateway next?