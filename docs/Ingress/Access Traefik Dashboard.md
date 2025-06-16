```bash
# Port forward to access Traefik dashboard
kubectl port-forward -n traefik-system service/traefik 9000:9000

# Then open browser to: http://localhost:9000/dashboard/

$ kubectl port-forward -n kube-system service/traefik 9000:9000
error: Service traefik does not have a service port 9000
```