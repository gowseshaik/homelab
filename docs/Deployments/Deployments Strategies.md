<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

Here's a table summarizing **Deployment Strategies** with the **What, Why, When, and How (W3H)** breakdown:  

| **Strategy**  | **What?** | **Why?** | **When?** | **How?** |
|--------------|----------|----------|----------|----------|
| **Rolling Update (Default)** | Gradually replaces old Pods with new ones in phases. | Ensures zero downtime during updates. | When high availability is critical (e.g., production environments). | Controlled via `maxUnavailable` (how many Pods can be down) and `maxSurge` (how many extra Pods can be created). |
| **Recreate** | Terminates all old Pods before creating new ones. | Ensures only one version runs at a time. | When the app cannot handle multiple versions running simultaneously (e.g., database schema changes). | Set `strategy.type: Recreate` in the Deployment spec. |
| **Blue-Green** | Deploys a new version alongside the old one, then switches traffic at once. | Minimizes risk and allows instant rollback. | When testing new versions before full release (e.g., canary testing). | Requires two identical environments (Deployments + Services). Switch traffic via Service selector update. |
| **Canary** | Slowly rolls out a new version to a subset of users. | Reduces risk by testing in production with real users. | When gradual validation is needed (e.g., A/B testing). | Use labels and selectors to route a portion of traffic to the new version. |
| **A/B Testing** | Routes traffic based on user attributes (headers, cookies). | Tests different features with real users. | When comparing multiple versions for performance or UX. | Requires Service Mesh (Istio, Linkerd) or Ingress controllers (Nginx, Traefik). |

| Type                  | Description                                                      |
| --------------------- | ---------------------------------------------------------------- |
| **Manual**            | Done by developer/admin, not automated                           |
| **Automated (CI/CD)** | Triggered by code pushes using Jenkins, GitHub Actions, etc.     |
| **Blue-Green**        | Two environments – switch traffic between them to avoid downtime |
| **Canary**            | Deploy to small % of users first, then gradually roll out        |
| **Rolling**           | Update instances gradually, one at a time                        |
| **Recreate**          | Stop old version completely, then deploy new one                 |
| **A/B Testing**       | Serve different app versions to test user response               |

### **Example Commands for Strategies**
#### **Rolling Update (Default)**
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1  # Only 1 Pod down at a time
      maxSurge: 1        # Only 1 extra Pod created
```

#### **Recreate Strategy**
```yaml
spec:
  strategy:
    type: Recreate
```

#### **Blue-Green Deployment (Manual Switch)**
```bash
# Deploy v1 (blue)
kubectl apply -f blue-deployment.yaml

# Deploy v2 (green)
kubectl apply -f green-deployment.yaml

# Switch traffic from blue to green
kubectl patch service myapp -p '{"spec":{"selector":{"version":"green"}}}'
```

#### **Canary Deployment (Partial Traffic)**
```bash
# Scale canary to 10% of traffic
kubectl scale deployment myapp-canary --replicas=2  # If main has 18 replicas (10%)
```

This table helps choose the right strategy based on **uptime requirements, risk tolerance, and testing needs**. 🚀