<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
```bash
# Port forward to access Traefik dashboard
kubectl port-forward -n traefik-system service/traefik 9000:9000

# Then open browser to: http://localhost:9000/dashboard/

$ kubectl port-forward -n kube-system service/traefik 9000:9000
error: Service traefik does not have a service port 9000
```