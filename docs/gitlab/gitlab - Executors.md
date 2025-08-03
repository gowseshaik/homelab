<span style="color:#4caf50;"><b>Created:</b> 2025-08-03</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-08-03</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

Lets learn, what **executors** are, and when you should choose each one, followed by a full table for comparison.

### 🔧 **What is an executor in GitLab Runner?**

An **executor** is the **environment or method GitLab Runner uses to run your CI/CD jobs**.

When you register a runner, it asks:  
**“How should I run your build jobs?”**  
That’s the executor.

### 🧠 How to choose the executor?

**Base it on:**

- Your infrastructure (bare-metal, VM, cloud, Kubernetes)
- Job requirements (Docker, Windows, parallelism, etc.)
- Isolation, scalability, speed, OS type

### 📋 Executor Comparison Table

|Executor|Use Case / When to Choose|OS Support|Isolation|Notes|
|---|---|---|---|---|
|`shell`|Simple, local builds on host OS (e.g., inside Multipass VM or bare-metal)|Linux/Windows|Low (host-level)|Fastest, but no isolation — shares file system|
|`docker`|You want isolated, containerized builds using Docker|Linux only|High|Most popular, supports caching, volumes, custom images|
|`docker+machine`|You want to autoscale runners with Docker Machine (cloud VM per job)|Linux|High|Deprecated by GitLab|
|`docker-windows`|Windows containers (rare)|Windows|High|Needs Docker on Windows|
|`docker-autoscaler`|Autoscale Docker runners with GitLab's autoscaler backend|Linux|High|GitLab's replacement for `docker+machine`|
|`custom`|You have a custom-built execution script or orchestration|Linux/Windows|Depends|Advanced use only — use your own tooling|
|`ssh`|Run jobs on remote servers via SSH|Linux/Windows|Medium|Useful for static remote runners (e.g., embedded or edge devices)|
|`virtualbox`|You want to run each job in a fresh VirtualBox VM|Any|High|Slow, but full VM isolation|
|`kubernetes`|CI/CD inside Kubernetes cluster (scalable, isolated pods)|Linux|Very High|Great for cloud-native setups|
|`parallels`|Run jobs on macOS VMs via Parallels|macOS|High|Only for Mac runners|
|`instance`|GitLab-provided (or cloud) VM provisioning — rare use|Linux|High|Part of GitLab SaaS (internal use usually)|

### 💡 Common Scenarios

|Scenario|Suggested Executor|
|---|---|
|Running in a Multipass or bare-metal Ubuntu|`shell`|
|You want job isolation & containerized CI|`docker`|
|You use Kubernetes cluster for builds|`kubernetes`|
|You run jobs on a remote machine|`ssh`|
|You have custom infrastructure|`custom`|
|You want auto-scaled runners|`docker-autoscaler`|
|You are on Windows or need Windows builds|`shell` or `docker-windows`|
# Recommend the best executors:

```json
Enter the GitLab instance URL: http://gitlab.local:8888/
Enter the registration token: <your_token>
Enter a description: multipass-runner
Enter tags: shell,local
Enter the executor: shell
```