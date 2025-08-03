<span style="color:#4caf50;"><b>Created:</b> 2025-08-03</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-08-03</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

```bash
#!/bin/bash

VM_NAME="gitlab-runner"
VM_CPUS=2
VM_MEM=2G
VM_DISK=20G

# 1. Launch Multipass VM
multipass launch --name $VM_NAME --cpus $VM_CPUS --mem $VM_MEM --disk $VM_DISK
```

### Create a runner in gitlab under CI/CD
```json
# Download the binary for your system
sudo curl -L --output /usr/local/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64

# Give it permission to execute
sudo chmod +x /usr/local/bin/gitlab-runner

# Create a GitLab Runner user
sudo useradd --comment 'GitLab Runner' --create-home gitlab-runner --shell /bin/bash

# Install and run as a service
sudo gitlab-runner install --user=gitlab-runner --working-directory=/home/gitlab-runner
sudo gitlab-runner start

# check the status of gitlab-runner
sudo gitlab-runner status

# gitlab-runner register
gitlab-runner register --url http://10.189.65.69:8888 --token glrt-TdgV8Xa-lkMLhdKPO0l-aG86MQp0OjdafaEKdToxCw.01.121bfaadavgu32

Enter the GitLab instance URL (for example, https://gitlab.com/):
http://<your_gitlab_vm_ip>:<port>

if it fails with "command not found"
rm ~/.gitlab-runner/config.toml
and try again

sudo gitlab-runner register --non-interactive \
  --url "http://10.189.65.69:8888" \
  --registration-token "glrt-TdgV8Xa-lkMLhdKPO0l-aG86MQp0OjEKdToxCw.01.121bvgu32" \
  --executor "shell" \
  --description "brmdev" \
  --tag-list "shell,brm" \
  --run-untagged="true" \
  --locked="false"
```

re-run
```bash
sudo gitlab-runner register --non-interactive \
  --url "http://10.189.65.69:8888" \
  --registration-token "glrt-TdgV8Xa-lkMLhdKPO0l-aG86MQp0OjEKdToxCw.01.121bvgu32" \
  --executor "shell" \
  --description "brmdev" \
  --tag-list "shell,brm" \
  --run-untagged="true" \
  --locked="false"


- now it went successful
```
# Recommend the best executors:

```json
Enter the GitLab instance URL: http://gitlab.local:8888/
Enter the registration token: <your_token>
Enter a description: multipass-runner
Enter tags: shell,local
Enter the executor: shell
```