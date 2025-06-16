```bash
#!/bin/bash

echo "=== Checking Traefik Helm Configuration ==="

# 1. Find Traefik release
echo "1. Finding Traefik Helm releases..."
helm list -A | grep traefik

# 2. Get Traefik values (replace namespace as needed)
echo -e "\n2. Getting Traefik Helm values..."
TRAEFIK_NAMESPACE=$(kubectl get pods -A | grep traefik | head -1 | awk '{print $1}')
TRAEFIK_RELEASE=$(helm list -A | grep traefik | head -1 | awk '{print $1}')

if [ ! -z "$TRAEFIK_RELEASE" ] && [ ! -z "$TRAEFIK_NAMESPACE" ]; then
    echo "Found Traefik release: $TRAEFIK_RELEASE in namespace: $TRAEFIK_NAMESPACE"
    
    echo -e "\n=== Current Traefik Values ==="
    helm get values $TRAEFIK_RELEASE -n $TRAEFIK_NAMESPACE
    
    echo -e "\n=== All Traefik Values (including defaults) ==="
    helm get values $TRAEFIK_RELEASE -n $TRAEFIK_NAMESPACE --all | grep -A 20 -B 5 "ports:\|entryPoints:\|tls:"
else
    echo "Traefik release not found via Helm"
fi

# 3. Check Traefik service ports
echo -e "\n3. Checking Traefik service configuration..."
kubectl get service -A | grep traefik
kubectl get service traefik -n $TRAEFIK_NAMESPACE -o yaml | grep -A 10 -B 5 "ports:"

# 4. Check for HTTPS/TLS configuration
echo -e "\n4. Checking for HTTPS/TLS configuration..."
kubectl get service traefik -n $TRAEFIK_NAMESPACE -o yaml | grep -E "443|websecure|tls"

# 5. Check Traefik deployment args
echo -e "\n5. Checking Traefik deployment arguments..."
kubectl get deployment traefik -n $TRAEFIK_NAMESPACE -o yaml | grep -A 20 "args:"

# 6. Check if Traefik dashboard is enabled
echo -e "\n6. Checking Traefik dashboard configuration..."
kubectl get deployment traefik -n $TRAEFIK_NAMESPACE -o yaml | grep -E "dashboard|api"

echo -e "\n=== Traefik Configuration Check Complete ==="
```