<span style="color:#4caf50;"><b>Created:</b> 2025-07-06</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
### ✅ **1. NGINX with Custom Config from ConfigMap**

**Use Case:** Inject a custom NGINX config via ConfigMap.

- **What to develop:** Pod running NGINX, config file (nginx.conf) mounted from ConfigMap.
    
- **What to test:** Change the ConfigMap, reload the pod, and see config take effect.

### ✅ **2. Python Flask App Reading Config via ENV (ConfigMap)**

**Use Case:** Pass app config (e.g., `APP_MODE=dev`) via environment variables.

- **What to develop:** Flask app that reads `APP_MODE` from `os.environ`.
    
- **What to test:** Update ConfigMap → redeploy → check changed behavior.

### ✅ **3. MySQL Pod with Password from Secret**

**Use Case:** Inject DB password using Kubernetes Secrets.

- **What to develop:** Pod running MySQL, `MYSQL_ROOT_PASSWORD` from a Secret.
    
- **What to test:** Try to connect using the injected password.

### ✅ **4. Node.js App Reading DB Credentials (ConfigMap + Secret)**

**Use Case:** Use both ConfigMap and Secret.

- ConfigMap → DB Host/Port
    
- Secret → DB username & password
    
- **What to test:** Print connection config in logs, verify secure loading.

### ✅ **5. Spring Boot App with Externalized Config**

**Use Case:** Use `application.properties` from a ConfigMap.

- Mount as file to `/config/application.properties`
    
- App reads from external config path

### ✅ **6. Static Web App (React/Angular) Using ConfigMap for API URL**

**Use Case:** Inject dynamic API endpoint using ConfigMap.

- Mount JSON file or inject via ENV at build/start
    
- Rebuild only when API endpoint changes
---

we can go with an example of **#4: Node.js App reading DB config from ConfigMap and Secret**.

### 📦 App Overview

- Simple Node.js Express app
    
- Reads DB config from:
    
    - `ConfigMap` → `DB_HOST`, `DB_PORT`
        
    - `Secret` → `DB_USER`, `DB_PASS`
        
- Prints values on `/config` endpoint

### 📁 1. **app.js**

```js
const express = require('express');
const app = express();

const config = {
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || '5432',
  user: process.env.DB_USER || 'user',
  pass: process.env.DB_PASS || 'pass',
};

app.get('/config', (req, res) => {
  res.json(config);
});

app.listen(3000, () => {
  console.log(`App running on port 3000`);
});
```

Explanation of above code.
```js
// Load the Express.js library to create a web server
const express = require('express');

// Create an instance of the Express application
const app = express();

// Define a config object that reads values from environment variables
// If a variable is not set, it uses a default fallback value
const config = {
  host: process.env.DB_HOST || 'localhost',     // DB host from ConfigMap or fallback to 'localhost'
  port: process.env.DB_PORT || '5432',          // DB port from ConfigMap or fallback to '5432'
  user: process.env.DB_USER || 'user',          // DB username from Secret or fallback to 'user'
  pass: process.env.DB_PASS || 'pass',          // DB password from Secret or fallback to 'pass'
};

// Define a GET endpoint '/config' to return the config values as JSON
app.get('/config', (req, res) => {
  res.json(config); // Send the config object as a JSON response
});

// Start the Express server on port 3000
app.listen(3000, () => {
  console.log(`App running on port 3000`); // Log a message when the server starts
});
```

---

### 🐳 2. **Dockerfile**

```Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY app.js .
RUN npm init -y && npm install express
CMD ["node", "app.js"]
```

---

### 🛠️ 3. **Kubernetes YAMLs**

#### 📘 `configmap.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: db-config
data:
  DB_HOST: postgres.dev.svc.cluster.local
  DB_PORT: "5432"
```

---

#### 🔐 `secret.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
stringData:
  DB_USER: admin
  DB_PASS: mysecretpass
```

---

#### 🚀 `deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: node-config-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: node-config-app
  template:
    metadata:
      labels:
        app: node-config-app
    spec:
      containers:
        - name: app
          image: node-config-app:latest
          ports:
            - containerPort: 3000
          env:
            - name: DB_HOST
              valueFrom:
                configMapKeyRef:
                  name: db-config
                  key: DB_HOST
            - name: DB_PORT
              valueFrom:
                configMapKeyRef:
                  name: db-config
                  key: DB_PORT
            - name: DB_USER
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: DB_USER
            - name: DB_PASS
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: DB_PASS
```

---

### 🌐 4. **Service (Optional)**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: node-config-svc
spec:
  selector:
    app: node-config-app
  ports:
    - port: 80
      targetPort: 3000
```

---

### 🧪 Test

```bash
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Port forward to test locally
kubectl port-forward svc/node-config-svc 8080:80

# Then open http://localhost:8080/config
```

