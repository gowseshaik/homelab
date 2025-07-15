| Option                  | Recommendation                                         |
| ----------------------- | ------------------------------------------------------ |
| `podman build --squash` | ✅ Native support                                       |
| `docker build --squash` | ⚠️ Supported, but only with experimental + no BuildKit |
| Multi-stage build       | ✅ Best practice for both Docker and Podman             |

| Feature                       | `docker commit`                     | `podman commit`                   |
| ----------------------------- | ----------------------------------- | --------------------------------- |
| ✅ Create image from container | ✅ Yes                               | ✅ Yes                             |
| 🧱 Squash layers              | ❌ No (not supported)                | ✅ `--squash` supported            |
| 🔐 Rootless support           | ❌ No (needs root unless configured) | ✅ Fully rootless                  |
| 🧾 Add metadata               | ✅ `--author`, `--message`           | ✅ Same                            |
| 🧪 OCI-compliant              | ✅ (with extra steps)                | ✅ Native                          |
| 🧰 Set image format           | ❌                                   | ✅ `--format=oci/docker`           |
| 🚀 Systemd-aware              | ❌                                   | ✅ Better integration with systemd |
| 🔍 Default history tracking   | ✅ via container diff                | ✅ via container diff              |
| 🧼 Clean image from temp      | ❌ manual                            | ✅ better layered FS support       |

| Scenario               | Use `docker commit` | Use `podman commit` |
| ---------------------- | ------------------- | ------------------- |
| One-time image capture | ✅ Yes               | ✅ Yes               |
| Reproducible CI builds | ❌ No                | ❌ No                |
| Secure release image   | ❌ No                | ✅ With `--squash`   |
| Rootless environments  | ❌ Limited           | ✅ Best option       |

### 🔧 **Dockerfile** (very basic):

```Dockerfile
# file: Dockerfile
FROM alpine:latest
RUN apk add --no-cache curl
RUN echo "hello world" > /hello.txt
```
### 🛠️ **Build Command**:

```bash
podman build --squash -t gowse/alpine-curl:v1 .
```

### 🧱 **Explanation **:

|Part|Meaning|
|---|---|
|`podman build`|Create an image from a Dockerfile|
|`--squash`|Combines all image layers into **one layer** (final image is smaller & cleaner)|
|`-t gowse/alpine-curl:v1`|Tags the image with a name and version|
|`.`|Build context is current directory (should contain Dockerfile)|

### ✅ Result:

- Final image has a **single layer** (no intermediate `RUN` layers).
- Smaller and cleaner image, better for production.

You're hitting a **real-world architectural pain point** that many large organizations face when dealing with **incremental container builds + integration-heavy runtimes** like **IBM App Connect Enterprise (ACE)**.

## 🎯 Problem Recap:

- You're continuously building and deploying **IBM App Connect containers**.
- Each **Integration Server (IS)** image has many **.bar workflows**.
- Over time, you **incrementally build** on top of previous Image Streams (possibly using S2I or `COPY`).
- Eventually, you're hitting this:

```text
error: max depth exceeded / too many layers
```

## 🧠 Deep Technical Cause (Layer Limit)

Each build adds **a new image layer**, especially if:

- You do **not squash**
- You **rebuild on top** of prior image streams (`FROM imageStreamName`)
- You add `.bar` files via separate `COPY`/`RUN` instructions.

You hit the **OverlayFS (OCI) limit**:

- Maximum = **125 layers** per image on `overlay2` (used by Docker, Podman, OpenShift)
- Many base images (e.g., ACE + Ubuntu) already have 10–30 layers
- Every new `COPY`, `RUN`, `.bar` deployment → new layer

⚠️ App Connect doesn’t do "one-bar-only" builds. So these accumulate fast.
## 🔍 Real Symptoms:

|Symptom|Root Cause|
|---|---|
|"Max layer/depth exceeded"|OCI spec violation due to too many `diff_ids` (layers)|
|App runs slow or crashes|Layer lookups degrade performance|
|Image push fails in CI/CD|Registry often rejects too deep manifest trees|
## ✅ `--squash`: Benefits for Your Case

|Benefit|Why It Matters for App Connect|
|---|---|
|💥 Removes all intermediate `.bar` layer diffs|You don't retain N history of bar files in FS layers|
|⬇️ Greatly reduces image layer count|You can continuously rebuild without hitting max layer|
|🔐 Hides sensitive integration flow stages (if any)|Good for regulatory reasons|
|💨 Smaller images = faster deploys across DEV/QA/PROD|Especially with remote registries|
|🧹 Prevents accumulation of dead bar versions|Since each squash is clean slate|
## ❌ Potential Downsides

|Risk|Mitigation|
|---|---|
|❌ Caching loss|Squashed images can't be layered on top of easily.|
|❌ Longer build times|Because everything builds from scratch|
|❌ Debuggability|Can’t `podman history` to inspect past layers|
|❌ Squash not supported in OpenShift S2I by default|You may need custom build scripts or `Containerfile` use|
## 🔄 Long-Term Strategy

### 🔧 Option 1: Use `--squash` for production deploys only

- **DEV:** Use normal layered builds for fast iteration
- **STAGE/PROD:** Use squashed images to avoid layer bloat
### 🔧 Option 2: Split Workflows by Domains

Instead of dumping 50 `.bar` files into one IS image:

- Break into **domain-specific Integration Servers**
    - `payments.is`, `orders.is`, `crm.is`
- Each one gets 5–10 bars max
- Now your `Dockerfile` looks like:

```Dockerfile
FROM ibm-appconnect:latest
COPY payment-flow1.bar /home/ace/ace-server/bars/
COPY payment-flow2.bar /home/ace/ace-server/bars/
```

- Less `.bar` layers = less layer growth over time

### 🔧 Option 3: Flatten image with custom script

Use a **build stage** that unpacks `.bar` files, copies them directly, then squashes.

```Dockerfile
FROM ibm-appconnect as builder
COPY *.bar /tmp/bars/
RUN for f in /tmp/bars/*.bar; do unpack-and-verify.sh "$f"; done

FROM scratch
COPY --from=builder /home/ace /home/ace
```
Then build with:
```bash
podman build --squash -t appconnect-integrations:v1 .
```

## 📊 Bonus: Audit Current Image Streams

```bash
oc get istag -n your-namespace
for tag in $(oc get istag -n your-namespace -o name); do
  echo "$tag: $(oc get "$tag" -o jsonpath='{.image.metadata.name}' | wc -l) layers"
done
```
Helps track which image stream has grown unacceptably large.
## 🎯 Final Recommendation

|Environment|Use `--squash`?|Notes|
|---|---|---|
|DEV|❌|Keep fast caching for rebuilds|
|QA / UAT|✅|Use squash to test realistic image|
|PROD|✅|Always squash to avoid image growth over time|

#### periodically clean up OpenShift ImageStreams to avoid bloating and hitting the layer limit:

## ✅ Goal:
- Clean up **old image tags** (ImageStreamTags)
- Prune **unused image layers** in registry
- Avoid **OCI layer depth limit**

## 🧼 1. Clean Up Old Tags in ImageStream (AppConnect IS)

### 🔁 Script to Keep Only Last N Tags:

```bash
#!/bin/bash
# keep last 5 tags in image stream
N=5
IMAGESTREAM=my-is-name
NAMESPACE=my-project

TAGS=$(oc get istag -n $NAMESPACE --sort-by=.metadata.creationTimestamp -o jsonpath="{range .items[*]}{.metadata.name}{'\n'}{end}" | grep "^$IMAGESTREAM:")

COUNT=$(echo "$TAGS" | wc -l)

if (( COUNT > N )); then
  DELETE_TAGS=$(echo "$TAGS" | head -n $((COUNT - N)))
  for tag in $DELETE_TAGS; do
    echo "Deleting tag: $tag"
    oc delete istag -n $NAMESPACE "$tag"
  done
fi
```

> 💡 Run this via **cronjob or Jenkins**.

## 🚮 2. Prune Unused Images from Internal Registry (Admin Only)

Run as cluster admin:
```bash
oc adm prune images \
  --keep-tag-revisions=3 \
  --keep-younger-than=72h \
  --confirm
```

|Option|Description|
|---|---|
|`--keep-tag-revisions=3`|Keep latest 3 image revisions per tag|
|`--keep-younger-than=72h`|Keep recent images (last 72 hours)|
|`--confirm`|Actually delete (omit for dry-run)|
> ⚠️ Only affects **internal OpenShift registry**.

## 🔍 3. Monitor Image Layer Depth per ImageStream

```bash
oc get istag -n your-namespace -o json | jq '.items[] | {name: .metadata.name, layers: .image.dockerImageLayers | length}'
```
## 🛡️ 4. Add CI/CD Rule to Prevent Deploying Images with Too Many Layers

In your Jenkins/CI:
```bash
LAYER_COUNT=$(podman history your-image | wc -l)

if (( LAYER_COUNT > 100 )); then
  echo "ERROR: Image has too many layers ($LAYER_COUNT). Deployment blocked."
  exit 1
fi
```
## 🗑️ 5. Optionally Remove ImageStream Manually

If certain ImageStreams are outdated:
```bash
oc delete is appconnect-is-old -n your-namespace
```

## 💡 Tips

|Tip|Benefit|
|---|---|
|Use `--squash` in QA/PROD images|Prevents future bloat|
|Automate `oc delete istag` by age/tag count|Keeps env clean|
|Use separate ImageStreams for DEV and PROD|Avoids dirty reuse|
|Run `oc adm prune images` weekly|Frees storage, resets layer chains|
#### production-ready OpenShift CronJob YAML to periodically **clean up old ImageStreamTags**, keeping only the latest **5 tags** in a given ImageStream.

## ✅ OpenShift CronJob: Cleanup Old Tags

### 📁 `imagestream-cleanup-cronjob.yaml`
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: imagestream-cleanup
  namespace: your-project
spec:
  schedule: "0 2 * * *"  # Every day at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: cleanup
            image: registry.redhat.io/openshift4/ose-cli  # OpenShift CLI image
            command:
            - /bin/bash
            - -c
            - |
              N=5
              IMAGESTREAM="your-image-stream-name"
              NAMESPACE="your-project"

              TAGS=$(oc get istag -n $NAMESPACE --sort-by=.metadata.creationTimestamp \
                -o jsonpath="{range .items[*]}{.metadata.name}{'\n'}{end}" | grep "^$IMAGESTREAM:")

              COUNT=$(echo "$TAGS" | wc -l)

              if (( COUNT > N )); then
                DELETE_TAGS=$(echo "$TAGS" | head -n $((COUNT - N)))
                for tag in $DELETE_TAGS; do
                  echo "Deleting $tag"
                  oc delete istag -n $NAMESPACE "$tag"
                done
              else
                echo "Nothing to delete. Total tags: $COUNT"
              fi
          restartPolicy: OnFailure
          serviceAccountName: imagestream-cleanup-sa
```

## 🔐 Service Account & Permissions

### 📁 `imagestream-cleanup-role.yaml`
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: imagestream-cleanup-sa
  namespace: your-project
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: imagestream-cleanup-role
  namespace: your-project
rules:
- apiGroups: ["image.openshift.io"]
  resources: ["imagestreamtags"]
  verbs: ["get", "list", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: imagestream-cleanup-binding
  namespace: your-project
subjects:
- kind: ServiceAccount
  name: imagestream-cleanup-sa
roleRef:
  kind: Role
  name: imagestream-cleanup-role
  apiGroup: rbac.authorization.k8s.io
```

## 🚀 Deploy in OpenShift
```bash
oc apply -f imagestream-cleanup-role.yaml
oc apply -f imagestream-cleanup-cronjob.yaml
```

## 📌 Notes

|Field|Description|
|---|---|
|`N=5`|Keeps only the latest 5 ImageStreamTags|
|`IMAGESTREAM`|Replace with your ACE Integration Server image stream name|
|`schedule`|Change to fit your cleanup window (e.g., `"0 */6 * * *"` for every 6h)|
|`ose-cli`|Lightweight Red Hat image with `oc` CLI for scripting|
