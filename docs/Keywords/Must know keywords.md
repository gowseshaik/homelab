<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
==**Ephemeral**== means **temporary** — it **exists only while the pod is running** and gets **deleted when the pod is deleted or restarted**.

| **Term**          | **Definition**                                                            |
| ----------------- | ------------------------------------------------------------------------- |
| **Ephemeral**     | Temporary — data or resource that disappears after session/pod is gone    |
| **Immutable**     | Cannot be changed after creation (e.g., Docker images, versioned infra)   |
| **Idempotent**    | Can be repeated with same result, no side effects (used in scripts, APIs) |
| **Stateless**     | Doesn’t store data between requests (all info comes from request itself)  |
| **Stateful**      | Stores data or state across sessions (e.g., databases, login sessions)    |
| **Orchestration** | Automated management of multiple containers/apps (e.g., Kubernetes)       |
| **Provisioning**  | Setting up infrastructure automatically (servers, storage, etc.)          |
| **Taint**         | Marking a node to repel certain pods (Kubernetes term)                    |
| **Toleration**    | Allowing a pod to be scheduled on a tainted node                          |
| **Throttling**    | Limiting usage of CPU/memory or API rate                                  |
| **Drain**         | Gracefully removing a node (evicts all pods) in Kubernetes                |
| **Scaling**       | Adding/removing resources (pods, instances) based on load                 |
| **Bootstrap**     | Initial setup process (e.g., first-time server config or cluster init)    |
| **Latency**       | Time delay between request and response                                   |
| **Throughput**    | Amount of data processed in a given time                                  |
| **Saturation**    | A resource being fully utilized (CPU, disk, etc.)                         |
| **Cold Start**    | First-time boot/load of an app/container; slower due to init time         |
| **Warm Start**    | Restart where some resources/state are already cached                     |
| **A/B Testing**   | Testing two versions of an app to compare performance                     |
| **Canary Deploy** | Releasing new version to a small group before full rollout                |

| **Image**                   | Read-only template used to create containers (like a snapshot of an app)              |
| --------------------------- | ------------------------------------------------------------------------------------- |
| **Container**               | Running instance of an image                                                          |
| **Registry**                | Storage/repository for container images (Docker Hub, Quay, GitHub Container Registry) |
| **Dockerfile**              | Text file with instructions to build a container image                                |
| **Layer**                   | Each step in a Dockerfile creates a filesystem layer                                  |
| **Volume**                  | Persistent storage that can be attached to containers                                 |
| **Bind Mount**              | Maps a directory from host into a container (live sync)                               |
| **Overlay Network**         | Docker’s network allowing containers to communicate across hosts                      |
| **Namespace**               | Linux kernel feature isolating container processes (PID, network, mount)              |
| **Cgroup**                  | Linux kernel feature limiting resource usage (CPU, memory) for containers             |
| **Entrypoint**              | Command that runs when container starts                                               |
| **CMD**                     | Default command/arguments for container; overridden by runtime command                |
| **Daemon**                  | Background service managing containers (Docker daemon or Podman service)              |
| **Pod**                     | Group of one or more containers sharing the same network/volume (Podman/K8s)          |
| **Image Tag**               | Version label of an image (e.g., `nginx:1.21`)                                        |
| **Docker Compose**          | Tool to define and run multi-container apps with YAML config                          |
| **Container Runtime**       | Software that runs containers (Docker, containerd, Podman, CRI-O)                     |
| **Build Context**           | Files and directories sent to daemon to build the image                               |
| **Entrypoint vs CMD**       | Entrypoint is fixed command, CMD is default args, CMD can override Entrypoint         |
| **Container Orchestration** | Managing multiple containers (e.g., Kubernetes, Docker Swarm)                         |
| **Sidecar Container**       | Helper container running alongside main container (logging, proxy)                    |
| **Rootless Mode**           | Running containers without root privileges (safer)                                    |
| **Image Pull**              | Downloading an image from a registry                                                  |
| **Image Push**              | Uploading a built image to a registry                                                 |
| **Container Snapshot**      | Saving the current state of a container as an image                                   |
| **Dangling Images**         | Unused images without tags, can be cleaned to free space                              |
| **Garbage Collection**      | Removing unused containers, images, volumes                                           |
