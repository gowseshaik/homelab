### 🔁 CI/CD Sync Failures & Misconfigurations

| Problem            | Why It Happens                                          | Impact                                     | Solution                                                                     |
| ------------------ | ------------------------------------------------------- | ------------------------------------------ | ---------------------------------------------------------------------------- |
| RBAC conflict      | ArgoCD lacks necessary roles on target namespaces       | Sync fails, app won’t deploy               | Bind ArgoCD SA (`argocd-application-controller`) to `edit` role in target NS |
| SA issues          | ArgoCD SA not authorized to manage cluster resources    | Permission denied errors                   | Ensure correct RBAC roles on both ArgoCD and app namespaces                  |
| Sync failures      | Manual drifts or cluster rejection (e.g., quota, SCC)   | Cluster state diverges from Git            | Enable auto-prune, fix invalid manifests, use `argocd app diff`              |
| Health check stuck | ArgoCD doesn’t recognize app’s health unless customized | App shows `Degraded` despite being healthy | Add custom health checks via ArgoCD app annotations                          |
### ☸️ Kubernetes/OpenShift Compatibility

|Problem|Why It Happens|Impact|Solution|
|---|---|---|---|
|Ingress vs Route mismatch|OpenShift uses `Route`, not `Ingress`|App not accessible externally|Use OpenShift Route CRDs instead of generic Ingress|
|Resource limit enforcement|OpenShift applies strict quota and limit ranges|Pod scheduling fails, app crashes|Add `resources.requests` and `resources.limits` in manifests|
|CrashLoopBackOff|Missing config maps, secrets, or bad probes|App stuck restarting|Use `kubectl describe pod` + logs to find actual cause|
|SCC violations|OpenShift enforces Security Context Constraints|Pod rejected by admission controller|Create custom SCC, bind to ArgoCD or app-specific SA|
|ArgoCD pod blocked|SCC or PSP restricts container permissions (e.g., root user)|ArgoCD can’t run apps with elevated needs|Use or create relaxed SCC for ArgoCD workloads|
### 🔐 Secrets Management

|Problem|Why It Happens|Impact|Solution|
|---|---|---|---|
|Secret mismatch in NS|Kubernetes secrets are namespace-scoped|ImagePull or app config fails|Ensure secrets exist and are correctly named in the app's namespace|
|Secrets in Git|Developers commit `.env` or YAML with sensitive data|Security risk (credentials exposed)|Use Bitnami SealedSecrets, SOPS, or Vault with ArgoCD plugin|
|Secret sync errors|Secrets are managed manually or by external systems|Drift between Git and actual state|Use GitOps-compatible secret generators or templates|
### 🛠️ Observability & Debugging

|Problem|Why It Happens|Impact|Solution|
|---|---|---|---|
|ArgoCD sync status unknown|Missing status info or failed sync hidden|Operators can't track deployment status|Use `argocd app sync`, `app wait`, and `argocd app history`|
|Logs missing or incomplete|Log aggregation not enabled or ArgoCD logs not visible|Hard to troubleshoot|Use `argocd app logs`, `kubectl logs`, or OpenShift console|
|Manifests differ|Rendered manifests not previewed|Unexpected cluster state|Use `argocd app manifests` and `argocd app diff` to compare|
### 🌐 Networking & Access

|Problem|Why It Happens|Impact|Solution|
|---|---|---|---|
|ArgoCD UI not accessible|Service not exposed via OpenShift Route|Cannot access ArgoCD Web UI|Use `oc expose svc/argocd-server -n argocd`|
|Ingress conflict with Route|Ingress.yaml conflicts with OpenShift Route behavior|Route override doesn’t work|Prefer Route CRD in manifests over Ingress|
|ArgoCD login errors|OAuth not integrated|Users must use local admin password|Use Dex with OpenShift OIDC or integrate with OpenShift OAuth provider|
### 💰 Resource Optimization

|Problem|Why It Happens|Impact|Solution|
|---|---|---|---|
|Orphaned resources|GitOps deletes missing resources only if auto-prune is enabled|Resource sprawl, cost waste|Enable `--auto-prune` on ArgoCD apps|
|Overprovisioned resources|Developers set excessive CPU/memory in manifests|Waste of capacity or throttling|Use `oc top pods` and tune HPA/limits accordingly|
|YAML duplication|No abstraction across environments|Difficult to manage & scale manifests|Use Kustomize or Helm with overlays per environment|
### 👥 Collaboration & Governance

|Problem|Why It Happens|Impact|Solution|
|---|---|---|---|
|No environment isolation|ArgoCD controls multiple environments with no boundaries|Accidental deploys to wrong namespaces|Use ArgoCD Projects to isolate apps, namespaces, repos|
|Manual change override|Cluster modified outside of GitOps|ArgoCD status out of sync|Enforce auto-sync with manual sync disabling + audit policy|
|Messy Git repo|No template abstraction, manual duplication|Error-prone, hard to scale|Use Helm, Kustomize, or Jsonnet for reusable manifests|
