| Task            | Command                               |
| --------------- | ------------------------------------- |
| Create chart    | `helm create <name>`                  |
| Install chart   | `helm install <release> <chart-path>` |
| Upgrade chart   | `helm upgrade <release> <chart-path>` |
| Uninstall chart | `helm uninstall <release>`            |
| Show values     | `helm show values <chart>`            |
| Validate chart  | `helm lint <chart-path>`              |
| Dry-run install | `helm install --dry-run --debug ...`  |
```
k delete all --all -n longhorn-system
k delete crds -l app.kubernetes.io/part-of=longhorn
k delete ns longhorn-system
helm uninstall longhorn -n longhorn-system || true
k get crds | grep longhorn

Then delete manually:
k delete crd <crd-name>
k get crds | grep longhorn | awk '{print $1}' | xargs k delete crd
k delete ns longhorn-system --grace-period=0 --force

If stuck in `Terminating`, run:
k get ns longhorn-system -o json | jq '.spec.finalizers=[]' | k replace --raw "/api/v1/namespaces/longhorn-system/finalize" -f -

Verify cleanup
k get crds | grep longhorn
k get ns | grep longhorn
```