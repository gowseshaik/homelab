<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

| Tool                         | Hosted Option      | Open Source | SCM Support       | Notes                              |
| ---------------------------- | ------------------ | ----------- | ----------------- | ---------------------------------- |
| **GitHub Actions**           | ✅ (GitHub)         | ❌           | GitHub only       | Free tier, integrated into GitHub  |
| **GitLab CI/CD**             | ✅ (GitLab)         | ✅           | GitLab            | Full DevOps suite                  |
| **Drone CI**                 | ✅                  | ✅           | GitHub, GitLab    | Lightweight, container-native      |
| **Woodpecker CI**            | ✅ (self-host)      | ✅           | GitHub, GitLab    | Drone fork, simple & fast          |
| **CircleCI**                 | ✅                  | ❌           | GitHub, Bitbucket | Free tier available                |
| **Argo CD / Argo Workflows** | ❌ (self-host only) | ✅           | GitOps-style      | Kubernetes-native workflows        |
| **Jenkins X**                | ✅ (via GCP)        | ✅           | GitHub, GitLab    | Jenkins for Kubernetes with GitOps |
| **Tekton**                   | ❌ (self-host)      | ✅           | Any               | Kubernetes-native pipelines        |
| **Buildkite**                | ✅                  | ❌           | GitHub, GitLab    | Agents run on your infra           |

|Tool|Hosting Type|Open Source|UI Available|Best For|
|---|---|---|---|---|
|**Woodpecker CI**|✅ Self-host|✅|✅ Web UI|Lightweight pipelines in Docker|
|**Drone CI**|✅ Self-host|✅|✅ Web UI|Container-native CI/CD|
|**GitLab CI/CD**|✅ GitLab-hosted|✅|✅ Full UI|Full DevOps pipelines|
|**Jenkins X**|✅ Self-host|✅|✅ (via UI)|Kubernetes + GitOps|
|**Argo Workflows**|✅ Self-host|✅|✅ Web UI|Kubernetes-native workflows|
|**Tekton + Dashboard**|✅ Self-host|✅|✅ Web UI|K8s-native, customizable|
|**Concourse CI**|✅ Self-host|✅|✅ Web UI|Pipeline-as-code, secure|
### 🔧 For **k3d/k3s**, recommended:

1. **Woodpecker CI** – lightweight, easy to set up with minimal resources.
2. **Drone CI** – native to containers, simple YAML pipelines.
3. **Argo Workflows** – great for Kubernetes-native automation.
4. **GitLab CE** – if you need an all-in-one platform.