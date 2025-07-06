<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

In Kubernetes, there are **three main types of load balancers** commonly used:

| Type                      | Description                                                            |
| ------------------------- | ---------------------------------------------------------------------- |
| **Internal LoadBalancer** | Used for internal services, only accessible within the cluster or VPC. |
| **External LoadBalancer** | Exposes services to the internet using a cloud provider’s external LB. |
| **Ingress Controller**    | Acts as a reverse proxy and manages HTTP/S traffic with routing rules. |

| LB Type | Layer  | Performance | Use Case                        |
| ------- | ------ | ----------- | ------------------------------- |
| ELB     | L4+L7  | Moderate    | Legacy/simple apps              |
| **NLB** | **L4** | **High**    | Real-time, fast apps like APIs  |
| ALB     | L7     | HTTP-aware  | Use with Ingress, not `Service` |
Additionally, you might use:

|Type|Description|
|---|---|
|**NodePort**|Exposes service on each node’s IP at a static port (not a full LB, but basic).|
|**MetalLB**|A load balancer implementation for bare metal clusters.|

### When and How to Use Internal vs External LoadBalancers

|Type|When to Use|How to Use|
|---|---|---|
|**Internal LoadBalancer**|For **intra-cluster** or **private** communication between services (e.g., backend APIs, internal DBs)|Use annotation to make it internal:`service.beta.kubernetes.io/aws-load-balancer-internal: "true"`|
|**External LoadBalancer**|When exposing a service to the **public internet** (e.g., front-end web app, public API)|Just define the service type as `LoadBalancer`, Kubernetes/cloud will handle provisioning.|

### Example YAMLs:

**Internal LoadBalancer (AWS/Azure/GCP-specific annotations):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-internal-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-internal: "true"
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
```

**External LoadBalancer:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-external-service
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
```

You're almost spot on — let me break it down clearly:
### ✅ Correct Understanding:

- **LoadBalancers work with Services**
    
- **Services route traffic to Pods**
    
- **Pods are created by Deployments (or StatefulSets, etc.)**
    
- So, **indirectly**, LoadBalancers affect traffic to Deployments via Services.

### ❌ But NOT directly tied to Deployment Strategies

- Deployment **strategies** like `RollingUpdate` or `Recreate` are just about **how pods are updated**
    
- LoadBalancers don’t care **how** or **when** the pods are created/updated — they just route to available, healthy pods via the Service.

---
### Flow Summary:

`LoadBalancer → Service → Pods ← Deployment (with strategy)`

- LoadBalancer: handles **external/internal traffic**
    
- Service: handles **routing logic**
    
- Deployment: manages **pod lifecycle**
    
- Strategy: manages **how pods get updated**, not how traffic is routed

So yes, they all work **together**, but the **LoadBalancer doesn’t depend on deployment strategy**.

In your **k3d cluster using Traefik**, you're using an **Ingress Controller**, which is a type of **Layer 7 (HTTP) Load Balancer**.

### Details:

|Component|Role|
|---|---|
|**Traefik**|Acts as an **Ingress Controller** (application-level load balancer)|
|**Ingress**|Defines routing rules (host/path based) to backend services|
|**Service**|Maps traffic from Traefik to Pods|
|**Deployment**|Manages Pods running your apps|

---

### So, the type of Load Balancer you're using is:

> ✅ **Ingress-based Load Balancer (via Traefik)**

It’s not a Service of type `LoadBalancer` (which works on cloud providers), but rather an **internal reverse proxy** that routes external traffic based on **Ingress rules**.

Here's a full list of commonly used **annotations for different types of LoadBalancers** across major cloud providers and Traefik:

---

### 🔹 **1. Internal LoadBalancer (Private)**

|Cloud|Annotation|
|---|---|
|**AWS**|`service.beta.kubernetes.io/aws-load-balancer-internal: "true"`|
|**Azure**|`service.beta.kubernetes.io/azure-load-balancer-internal: "true"`|
|**GCP**|`cloud.google.com/load-balancer-type: "Internal"`|

---

### 🔹 **2. External LoadBalancer (Public)**

_(These are usually default; no annotation needed, but here’s how to customize)_

|Cloud|Annotation Example|
|---|---|
|**AWS**|`service.beta.kubernetes.io/aws-load-balancer-type: "nlb"` (or "elb")|
|**Azure**|`service.beta.kubernetes.io/azure-load-balancer-internal: "false"`|
|**GCP**|`cloud.google.com/load-balancer-type: "External"` _(default)_|

---

### 🔹 **3. Ingress-based LoadBalancer (e.g., Traefik)**

|Use Case|Annotation|
|---|---|
|**Traefik IngressClass**|`kubernetes.io/ingress.class: "traefik"`|
|**TLS redirection**|`traefik.ingress.kubernetes.io/redirect-entry-point: https`|
|**Rewrite Path**|`traefik.ingress.kubernetes.io/rewrite-target: /`|

---

### 🔹 **4. MetalLB (for bare metal / local)**

|Use Case|Annotation|
|---|---|
|**Assign static IP**|`metallb.universe.tf/address-pool: "default"`|

---
Great — here are **ready-to-use YAML examples with annotations** for each type of LoadBalancer based on your setup:

---

## 🔸 **1. AWS**

### ✅ External LoadBalancer (Public)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-public-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
```

### ✅ Internal LoadBalancer (Private)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-internal-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-internal: "true"
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
```

---

## 🔸 **Azure**

### ✅ Internal LoadBalancer

```yaml
metadata:
  name: my-internal-azure-svc
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"
```

---

## 🔸 **GCP**

### ✅ Internal LoadBalancer

```yaml
metadata:
  name: my-internal-gcp-svc
  annotations:
    cloud.google.com/load-balancer-type: "Internal"
```

---

## 🔸 **MetalLB (Local/Bare Metal)**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-metallb-service
  annotations:
    metallb.universe.tf/address-pool: "default"
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
```

---

## 🔸 **Traefik Ingress (for your k3d setup)**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-traefik-ingress
  annotations:
    kubernetes.io/ingress.class: "traefik"
    traefik.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - host: myapp.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-service
                port:
                  number: 80
```

### 🔹 What is `nlb` in AWS Annotation?

`nlb` stands for **Network Load Balancer** in AWS. It’s a high-performance, Layer 4 (TCP/UDP) load balancer that handles **millions of requests per second with low latency**.

---

### 🔹 AWS Annotation Meaning:

```yaml
service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
```

This tells Kubernetes to create an **AWS Network Load Balancer (NLB)** instead of the default **Classic Load Balancer (ELB)**.

|LB Type|Layer|Performance|Use Case|
|---|---|---|---|
|ELB|L4+L7|Moderate|Legacy/simple apps|
|**NLB**|**L4**|**High**|Real-time, fast apps like APIs|
|ALB|L7|HTTP-aware|Use with Ingress, not `Service`|

---

### 🔹 Are These Services Predefined?

No — these are **not predefined**. When you create a `Service` of type `LoadBalancer`, **Kubernetes asks the cloud provider** (via the Cloud Controller Manager) to provision a real load balancer resource **dynamically**.

---

### 🔹 Creation Process (Simplified):

1. You define a `Service` with `type: LoadBalancer`
    
2. Kubernetes talks to the **cloud provider API**
    
3. The cloud creates:
    
    - A load balancer (ELB, NLB, etc.)
        
    - Configures listeners and target groups
        
    - Maps it to the appropriate nodes/pods
        
4. The LB's **public or private IP** is reflected in the service status (`EXTERNAL-IP`)
    

---

### 🔹 So, You Control:

- Type (`LoadBalancer`, `ClusterIP`, `NodePort`)
    
- Provider behavior via **annotations**
    
- Target pods via **selectors**
    
- Protocols via **ports**
    

Let me know if you want a visual flow or deeper dive into a specific cloud (e.g., NLB with TLS, ALB via Ingress, etc.).