<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
```
podman save -o ubi-unzip.tar localhost/ubi-unzip:latest

upload to remote host, offline On Remote Host:
podman load -i ubi-unzip.tar
```