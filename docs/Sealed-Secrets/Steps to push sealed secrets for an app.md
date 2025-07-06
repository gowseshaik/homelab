<span style="color:#4caf50;"><b>Created:</b> 2025-07-06</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
```bash
# Example: Practical GitOps flow to push sealed secrets for an app config

# 1. Prepare plain secret YAML locally
cat > secret.yaml <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
  namespace: default
type: Opaque
data:
  db_user: YWRtaW4=        # base64 for 'admin'
  db_password: c2VjdXJl   # base64 for 'secure'
EOF

# 2. Seal the secret with kubeseal using cluster public key
kubectl create -f secret.yaml --dry-run=client -o json | kubeseal --format yaml > sealed-secret.yaml

# 3. Initialize Git repo or navigate to your GitOps repo directory
git init my-gitops-repo
cd my-gitops-repo

# 4. Copy sealed secret to the repo folder
cp ../sealed-secret.yaml ./sealed-secret.yaml

# 5. Commit and push to remote Git repo (GitHub/Gitea)
git add sealed-secret.yaml
git commit -m "Add sealed secret for app"
git remote add origin git@github.com:youruser/yourrepo.git
git push -u origin main

# 6. Apply manifests from GitOps pipeline or manually trigger a sync (e.g. ArgoCD/Flux)
# Cluster will automatically decrypt sealed-secret.yaml and create the actual secret.

```

> **Notes:**
> 
> - You run `kubeseal` locally or in CI before pushing to Git.
> - The Git repo stores only encrypted secrets.
> - The cluster controller decrypts and creates Kubernetes secrets.
> - Use this with GitOps tools like ArgoCD or Flux for automated syncing.