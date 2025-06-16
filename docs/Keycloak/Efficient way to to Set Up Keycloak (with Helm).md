Here's the most efficient way to set up Keycloak on a Kubernetes/OpenShift cluster using the official Helm chart.

---

### ✅ **Steps to Set Up Keycloak (with Helm)**

1. **Add Bitnami repo**
    
    ```bash
    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm repo update
    ```
    
2. **Create namespace**
    
    ```bash
    kubectl create namespace keycloak
    ```
    
3. **Install Keycloak**
Yes — since you're using **k3d with the default Traefik ingress controller**, you should expose Keycloak via an **Ingress**.

---

### ✅ Steps to Create Ingress for Keycloak on k3d with Traefik

1. **Install Keycloak with hostname**
 ```bash
    helm install keycloak bitnami/keycloak -n keycloak \
      --set auth.adminUser=admin \
      --set auth.adminPassword=adminpassword \
      --set service.type=ClusterIP \
      --set ingress.enabled=true \
      --set ingress.hostname=keycloak.local \
      --set ingress.annotations."traefik\.ingress\.kubernetes\.io/router\.entrypoints"=web

helm install keycloak bitnami/keycloak -n keycloak \
      --set auth.adminUser=admin \
      --set auth.adminPassword=admin123 \
      --set service.type=ClusterIP \
      --set ingress.enabled=true \
      --set ingress.hostname=keycloak.local \
      --set ingress.annotations."traefik\.ingress\.kubernetes\.io/router\.entrypoints"=web
```


```bash
gouse@gouse:~/DevOps/k3d$ helm install keycloak bitnami/keycloak -n keycloak \
      --set auth.adminUser=admin \
      --set auth.adminPassword=admin123 \
      --set service.type=ClusterIP \
      --set ingress.enabled=true \
      --set ingress.hostname=keycloak.local \
      --set ingress.annotations."traefik\.ingress\.kubernetes\.io/router\.entrypoints"=web
NAME: keycloak
LAST DEPLOYED: Mon Jun  9 18:31:36 2025
NAMESPACE: keycloak
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: keycloak
CHART VERSION: 24.7.3
APP VERSION: 26.2.5

Did you know there are enterprise versions of the Bitnami catalog? For enhanced secure software supply chain features, unlimited pulls from Docker, LTS support, or application customization, see Bitnami Premium or Tanzu Application Catalog. See https://www.arrow.com/globalecs/na/vendors/bitnami for more information.

** Please be patient while the chart is being deployed **

Keycloak can be accessed through the following DNS name from within your cluster:

    keycloak.keycloak.svc.cluster.local (port 80)

To access Keycloak from outside the cluster execute the following commands:

1. Get the Keycloak URL and associate its hostname to your cluster external IP:

   export CLUSTER_IP=$(minikube ip) # On Minikube. Use: `kubectl cluster-info` on others K8s clusters
   echo "Keycloak URL: http://keycloak.local/"
   echo "$CLUSTER_IP  keycloak.local" | sudo tee -a /etc/hosts

2. Access Keycloak using the obtained URL.
3. Access the Administration Console using the following credentials:

  echo Username: admin
  echo Password: $(kubectl get secret --namespace keycloak keycloak -o jsonpath="{.data.admin-password}" | base64 -d)

WARNING: There are "resources" sections in the chart not set. Using "resourcesPreset" is not recommended for production. For production installations, please set the following values according to your workload needs:
  - resources
+info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

```

    
2. **Add host entry (on your machine)**
    
    ```bash
    echo "127.0.0.1 keycloak.local" | sudo tee -a /etc/hosts
    get the ip from ingress deployed for keycloak
    echo "172.18.0.2 keycloak.local" | sudo tee -a /etc/hosts
    ```
    
3. **Check ingress is created**
    
    ```bash
    kubectl get ingress -n keycloak
    ```
    
4. **Access Keycloak**
    
    - Open browser: [http://keycloak.local](http://keycloak.local)
        

---

Let me know if you need HTTPS (TLS) setup with Traefik too.