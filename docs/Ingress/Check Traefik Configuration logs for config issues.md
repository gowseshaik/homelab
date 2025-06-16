```bash
# Check Traefik deployment
kubectl get deployment traefik -n traefik-system -o yaml

# Check Traefik service (look for ports configuration)
kubectl get service traefik -n traefik-system -o yaml

# Check Traefik ConfigMap (if using static configuration)
kubectl get configmap -n traefik-system
kubectl describe configmap traefik-config -n traefik-system  # if exists

# Check Traefik pods
kubectl get pods -n traefik-system
kubectl describe pod traefik-xxx-xxx -n traefik-system
```

# Check Traefik Logs for Configuration Issues
```bash
# Check Traefik logs
kubectl logs -n traefik-system deployment/traefik

# Follow logs in real-time
kubectl logs -n traefik-system deployment/traefik -f

# Check for specific configuration errors
kubectl logs -n traefik-system deployment/traefik | grep -i "error\|warn\|config"
```

