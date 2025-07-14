### ✅ Basic Syntax:
```bash
docker build https://github.com/username/repo.git#branch:folder-path -t image-name:tag
```
### ✅ Example:
```bash
docker build https://github.com/nginxinc/docker-nginx.git#main:stable -t my-nginx:latest
```

```
docker build https://github.com/user/repo.git#branch:subdir -t ttl.sh/image-name:1h && docker push ttl.sh/image-name:1h

docker build https://github.com/nginxinc/docker-nginx.git#main:stable -t ttl.sh/nginx-test:1h && docker push ttl.sh/nginx-test:1h
```

|Placeholder|Meaning|
|---|---|
|`user/repo.git`|Your GitHub repo|
|`#branch:subdir`|(optional) Git branch and subdir with Dockerfile|
|`ttl.sh/image-name:1h`|TTL image name with expiry (e.g., 1h, 30m, 1d)

### 🧾 Options:

| Git Source Format        | Description                             |
| ------------------------ | --------------------------------------- |
| `repo.git`               | Default branch and root directory       |
| `repo.git#branch`        | Specific branch                         |
| `repo.git#:subdir`       | Specific subdirectory in default branch |
| `repo.git#branch:subdir` | Specific branch and subdirectory        |

---
### ✅ Notes:
- Git repo must have a `Dockerfile` at root or in specified path.
- `git` must be installed on your system.
- You can pass `-f` to specify custom `Dockerfile`:

```bash
docker build -f Dockerfile.dev https://github.com/user/repo.git#branch -t custom-image
```

if the `Dockerfile` is **not** in the root of the Git repo, **you must specify the correct subdirectory path**. Otherwise, Docker will fail with:

> `unable to prepare context: unable to find a Dockerfile`
