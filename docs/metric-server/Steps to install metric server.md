<span style="color:#4caf50;"><b>Created:</b> 2025-08-03</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-08-03</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

Step 1:
```
$ kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

```bash
$ k get all -A
NAMESPACE    NAME                                READY STATUS  RESTARTS  AGE
kube-system  pod/metrics-server-64c95ff7bb-gw692  0/1  Running      0     32s

$ k describe pod metrics-server-64c95ff7bb-gw692
Events:
  Type     Reason     Age               From               Message
  ----     ------     ----              ----               -------
  Normal   Scheduled  51s               default-scheduler  Successfully assigned kube-system/metrics-server-64c95ff7bb-gw692 to int-cluster-control-plane
  Normal   Pulling    52s               kubelet            Pulling image "registry.k8s.io/metrics-server/metrics-server:v0.8.0"
  Normal   Pulled     45s               kubelet            Successfully pulled image "registry.k8s.io/metrics-server/metrics-server:v0.8.0" in 6.406172997s (6.406182876s including waiting)
  Normal   Created    45s               kubelet            Created container metrics-server
  Normal   Started    45s               kubelet            Started container metrics-server
  Warning  Unhealthy  2s (x3 over 22s)  kubelet            Readiness probe failed: HTTP probe failed with statuscode: 500
```

The `Readiness probe failed: HTTP probe failed with statuscode: 500` usually means **Metrics Server is running** but **can't scrape metrics from kubelets** — even after adding `--kubelet-insecure-tls`.

### ✅ Fix: Patch all required args explicitly

Kind clusters often require **multiple flags**. Apply this **one-shot full patch**:

```bash
kubectl patch deployment metrics-server -n kube-system --type='json' -p='[
  {"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-preferred-address-types=InternalIP"},
  {"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}
]'
```

Then **restart the pod** to force changes:

```bash
kubectl delete pod -n kube-system -l k8s-app=metrics-server
```

---

### Verify:

```bash
kubectl top nodes
kubectl top pods -A
```

---

Let me know if it still fails — I’ll give a complete working manifest override for Kind.