| Principle               | **NGINX**  | **HAProxy** | **Traefik**   | **Kong**           | **Istio Gateway**  |
| ----------------------- | ---------- | ----------- | ------------- | ------------------ | ------------------ |
| Traffic Entry           | ✅ Yes      | ✅ Yes       | ✅ Yes         | ✅ Yes              | ✅ Yes              |
| Path/Host Routing       | ✅ Basic    | ✅ Basic     | ✅ Advanced    | ✅ Advanced         | ✅ Advanced (Envoy) |
| TLS Termination         | ✅ Yes      | ✅ Yes       | ✅ Yes         | ✅ Yes              | ✅ Yes              |
| Request Auth            | ❌ (plugin) | ❌           | ✅ Middleware  | ✅ JWT/OIDC Plugins | ✅ Native JWT       |
| Rate Limiting           | ❌ (plugin) | ❌           | ✅ Middleware  | ✅ Native           | ✅ Policy-based     |
| Metrics/Logging         | 🟡 Basic   | 🟡 Basic    | ✅ Prometheus  | ✅ Plugins          | ✅ Envoy Metrics    |
| Dynamic Config Reload   | ❌ (reload) | ❌ (reload)  | ✅ Hot reload  | ✅ CRDs             | ✅ Envoy xDS        |
| Plugin Ecosystem        | ❌          | ❌           | ✅ Middlewares | ✅ Strong Plugins   | ❌ No plugins       |
| Mesh/Zero Trust Support | ❌          | ❌           | ❌             | ❌                  | ✅ Full support     |
## ✅ What to pick

| Need                                        | Best Option |
| ------------------------------------------- | ----------- |
| Simple, stable ingress                      | **NGINX**   |
| High performance, low memory                | **HAProxy** |
| Dynamic routing + modern DevOps             | **Traefik** |
| API gateway + plugin-based auth             | **Kong**    |
| Zero trust + mesh + advanced routing/policy | **Istio**   |

|Ingress Controller|Pros|Cons|Pricing|
|---|---|---|---|
|**NGINX Ingress**|Widely used, well-documented, flexible config, supports custom rules|Limited advanced routing, lower performance at scale|Free (Open Source), **NGINX Plus** is commercial (~$2,500/year/node)|
|**HAProxy Ingress**|High performance, low latency, advanced routing|Smaller community, fewer features than NGINX|Free (Open Source), Enterprise support available (custom pricing)|
|**Traefik**|Auto-discovery, native K8s, easy dashboard|Learning curve, fewer advanced features vs. NGINX|Free (Open Source), Traefik Enterprise (starts ~$2,000/year)|
|**Istio Ingress Gateway**|Deep integration with service mesh, security features (mTLS, etc.)|Heavy, complex to configure and manage|Free (Open Source)|
|**Kong Ingress Controller**|API Gateway features, plugins, scalability|Paid features gated in Enterprise version|OSS free, **Kong Enterprise** (starts ~$2,500+/year)|
|**AWS ALB Ingress**|Managed by AWS, auto-scalable, native integration|AWS only, slower config propagation|Pay-per-use (based on ALB usage - ~$0.0225/hr + LCU costs)|
|**GKE Ingress (Google)**|Managed, autoscaling, native GCP integration|GCP only, limited customization|Free tier + Pay-per-use (based on Load Balancer usage)|
|**Azure Application Gateway Ingress**|Native Azure integration, WAF support|Azure only, limited custom routing|Pay-per-use (~$0.008/hr + data processing fees)|
|**Ambassador Edge Stack**|API Gateway features, easy developer interface|Full features need paid version|OSS free, **Enterprise** (starts ~$3,000+/year)|
|**Contour**|Built on Envoy, fast updates, CRD support|Smaller community, fewer features than Istio or NGINX|Free (Open Source)|

Let me know if you want a filtered list for cloud-native, performance-focused, or self-hosted only.