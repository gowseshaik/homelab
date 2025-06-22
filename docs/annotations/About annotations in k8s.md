## ✅ What are annotations?

- Annotations are key-value pairs used to attach **non-identifying metadata** to Kubernetes objects.
- Unlike labels (used for selection/filtering), annotations are used for **descriptive** or **informational** purposes.

## 🕒 When to use annotations?

Use annotations when:

- You need to **store metadata** that doesn't affect how Kubernetes manages the object.
- You want to **document context**, **track changes**, or **pass info to tools/controllers**.

**Examples:**
- Add build info, commit hash, owner, team
- Store debugging or troubleshooting info
- Track last edited by whom, when, and why
- Set instructions for custom controllers or operators

## ❓Why use annotations?
- They don't affect scheduling, selectors, or object behavior (unlike labels).
- They’re perfect for **audit trails**, **history**, and **external tools**.
- Clean way to **embed business context** inside manifests.
- Helps for **DevOps transparency** and **team collaboration**.

## ⚙️ How to use annotations?

### 1. **CLI**

```bash
kubectl annotate pod mypod key=value
kubectl annotate pod mypod owner="gowse" purpose="debugging"
kubectl annotate pod mypod purpose-
```

### 2. **YAML**

```yaml
metadata:
  annotations:
    owner: "gowse"
    purpose: "troubleshooting"
```

### 3. **Use Cases**

|Use Case|Key Example|
|---|---|
|Git metadata|git.commit=abc123|
|Owner tracking|owner=gowse|
|Change reason|w3h.why="updated image to fix bug"|
|Debug instructions|w3h.how="enable debug logging in config"|
|Triggering CI/CD tools|build.trigger=manual|
|Custom controller hints|sidecar-injector.k8s.io/inject: "true"|
