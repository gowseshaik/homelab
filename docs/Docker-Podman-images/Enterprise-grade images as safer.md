<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

Yes, it's **normal** for UBI (Universal Base Image) images to increase a bit in size when adding packages like `unzip`.
### 📌 Details:

- **Base UBI Image**: `213 MB`
- **After installing `unzip`**: `228 MB` ➝ ✅ **only +15 MB**
- That’s a **reasonable and expected** increase.

### 🧠 Why not aggressively reduce size here:

- **UBI is meant for Red Hat compatibility** and enterprise-grade support.
- You keep `dnf` and required system libs which add size.
- Stripping too much (like removing `dnf`, locale files, etc.) may **break** system tooling or future updates.
 
### ✅ Best practices (already covered in your Dockerfile):

- `dnf clean all` ✅
- `rm -rf /var/cache/dnf` ✅
You already did the right optimizations.

### ✅ If you want **minimal base image** with just unzip:

You can consider using `alpine`:
```Dockerfile
FROM alpine:3.20
RUN apk add --no-cache unzip
WORKDIR /app
CMD ["sh"]
```

**Size**: ~6 MB  
But **not compatible with RHEL environments or UBI policies**.

### 🔍 Summary

|Option|Base Size|Final Size|Notes|
|---|---|---|---|
|`ubi8/ubi`|~213 MB|~228 MB|✅ Safe, supported, expected size|
|`alpine`|~5 MB|~6–7 MB|⚠️ Smaller but not RHEL-compatible|
So for enterprise or UBI environments, your image is fine. No need to reduce further.