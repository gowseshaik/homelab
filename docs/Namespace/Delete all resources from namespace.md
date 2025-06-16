Run the following command to delete **all resources** in a namespace:

```bash
kubectl delete all --all -n demo
```

To also delete **configmaps, secrets, PVCs, etc.**, run:

```bash
kubectl delete all,cm,secret,pvc,ingress,role,rolebinding,serviceaccount --all -n demo
```

Or to **delete the entire namespace** (which deletes everything inside):

```bash
kubectl delete namespace demo
```