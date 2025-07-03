[Rajesh Kumar](https://www.devopsschool.com/blog/author/rajeshkumar/ "Posts by Rajesh Kumar") April 2, 2023 [Leave a Comment](https://www.devopsschool.com/blog/deploy-ha-kubernetes-cluster-on-linux-using-rancher-rke2/#respond)

Table of Contents

[](https://www.devopsschool.com/blog/deploy-ha-kubernetes-cluster-on-linux-using-rancher-rke2/#)

- [What is RKE2?](https://www.devopsschool.com/blog/deploy-ha-kubernetes-cluster-on-linux-using-rancher-rke2/#What_is_RKE2)
    - [System Requirements](https://www.devopsschool.com/blog/deploy-ha-kubernetes-cluster-on-linux-using-rancher-rke2/#System_Requirements)
- [Step 1 – Set up Rocky Linux 8 Nodes](https://www.devopsschool.com/blog/deploy-ha-kubernetes-cluster-on-linux-using-rancher-rke2/#Step_1_%E2%80%93_Set_up_Rocky_Linux_8_Nodes)
- [Step 2 – Configure the Fixed Registration Address](https://www.devopsschool.com/blog/deploy-ha-kubernetes-cluster-on-linux-using-rancher-rke2/#Step_2_%E2%80%93_Configure_the_Fixed_Registration_Address)
- [Step 3 – Download installer script on Rocky Linux 8 Nodes](https://www.devopsschool.com/blog/deploy-ha-kubernetes-cluster-on-linux-using-rancher-rke2/#Step_3_%E2%80%93_Download_installer_script_on_Rocky_Linux_8_Nodes)
- [Step 4 – Set up the First Server Node (Master Node)](https://www.devopsschool.com/blog/deploy-ha-kubernetes-cluster-on-linux-using-rancher-rke2/#Step_4_%E2%80%93_Set_up_the_First_Server_Node_Master_Node)
- [Step 7 – Deploy an Application.](https://www.devopsschool.com/blog/deploy-ha-kubernetes-cluster-on-linux-using-rancher-rke2/#Step_7_%E2%80%93_Deploy_an_Application)
- [Reference](https://www.devopsschool.com/blog/deploy-ha-kubernetes-cluster-on-linux-using-rancher-rke2/#Reference)

## What is RKE2?

RKE stands for **Rancher Kubernetes Engine**. RKE2 also known as the (RKE Government) is a combination of RKE1 and K3s. It inherits usability, ease-of-operations, and deployment model from K3s and close alignment with upstream Kubernetes from RKE1. Normally, RKE2 doesn’t rely on docker, it launches the control plane components as static pods that are managed by the kubelet.

The diagram below will help you understand the RKE2 cluster topology.

![](https://www.devopsschool.com/blog/wp-content/uploads/2023/04/image-4-1024x372.png)

RKE2 ships a number of open-source components that include:

- K3s
    - Helm Controller
- K8s
    - API Server
    - Controller Manager
    - Kubelet
    - SchedulerSet up Linux Nodes
    - Proxy
- etcd
- containerd/cri
- runc
- Helm
- Metrics Server
- NGINX Ingress Controller
- CoreDNS
- CNI: Canal (Calico & Flannel), Cilium or Calico

### System Requirements

Use a system that meets the below requirements:

- RAM: 4GB Minimum (we recommend at least 8GB)
- CPU: 2 Minimum (we recommend at least 4CPU)
- 3 Rocky Linux 8 Nodes
- **Zero** or _more agent_ nodes that are designated to run your apps and services
- A **load balancer** to direct front-end traffic to the three nodes.
- A **DNS record** to map a URL to the load balancer

## Step 1 – Set up Rocky Linux 8 Nodes

For this guide, we will use 3 Rocky Linux nodes, a load balancer, and RKE2 agents(1 or more).

|   |   |   |
|---|---|---|
|**TASK**|**HOSTNAME**|**IP** **ADDRESS**|
|_Server Node 1_|_server1.computingforgeeks.com_|192.168.205.2|
|_Server Node 2_|_server2.computingforgeeks.com_|192.168.205.3|
|_Server Node_ 3|_server3.computingforgeeks.com_|192.168.205.33|
|_Load Balancer_|_rke.computingforgeeks.com_|192.168.205.9|
|_Agent Node1_|_agent1.computingforgeeks.com_|192.168.205.43|
|_Agent Node2_|_agent2.computingforgeeks.com_|192.168.205.44|

Set the hostnames as shown:

![](https://www.devopsschool.com/blog/wp-content/uploads/2023/04/image-5.png)

Add the hostnames to /etc/hosts on each node

![](https://www.devopsschool.com/blog/wp-content/uploads/2023/04/image-6.png)

Configure the firewall on all the nodes as shown:

![](https://www.devopsschool.com/blog/wp-content/uploads/2023/04/image-7.png)

## Step 2 – Configure the Fixed Registration Address

To achieve high availability, you are required to set up an odd number of server plane nodes(runs etcd, the Kubernetes API, and other control plane services). The other server nodes and agent nodes need a URL they can use to register against. This is either an IP or domain name of any of the control nodes. This is mainly done to maintain quorum so that the cluster can afford to lose connection with one of the nodes without impacting the functionality cluster.

This can be achieved using the following:

- A layer 4 (TCP) load balancer
- Round-robin DNS
- Virtual or elastic IP addresses

In this guide, we will configure NGINX as a layer 4 (TCP) load balancer to forward the connection to one of the RKE nodes.

![](https://www.devopsschool.com/blog/wp-content/uploads/2023/04/image-8.png)

---

```
user nginx;
worker_processes 4;
worker_rlimit_nofile 40000;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 8192;
}

stream {
upstream backend {
        least_conn;
        server <IP_NODE_1>:9345 max_fails=3 fail_timeout=5s;
        server <IP_NODE_2>:9345 max_fails=3 fail_timeout=5s;
        server <IP_NODE_3>:9345 max_fails=3 fail_timeout=5s;
   }

   # This server accepts all traffic to port 9345 and passes it to the upstream. 
   # Notice that the upstream name and the proxy_pass need to match.
   server {

      listen 9345;

          proxy_pass backend;
   }
    upstream rancher_api {
        least_conn;
        server <IP_NODE_1>:6443 max_fails=3 fail_timeout=5s;
        server <IP_NODE_2>:6443 max_fails=3 fail_timeout=5s;
        server <IP_NODE_3>:6443 max_fails=3 fail_timeout=5s;
    }
        server {
        listen     6443;
        proxy_pass rancher_api;
        }
    upstream rancher_http {
        least_conn;
        server 192.168.205.2:80 max_fails=3 fail_timeout=5s;
        server 192.168.205.3:80 max_fails=3 fail_timeout=5s;
        server 192.168.205.33:80 max_fails=3 fail_timeout=5s;
    }
        server {
        listen     80;
        proxy_pass rancher_http;
        }
    upstream rancher_https {
        least_conn;
        server 192.168.205.2:443 max_fails=3 fail_timeout=5s;
        server 192.168.205.3:443 max_fails=3 fail_timeout=5s;
        server 192.168.205.33:443 max_fails=3 fail_timeout=5s;
    }
        server {
        listen     443;
        proxy_pass rancher_https;
        }
}
```

---

![](https://www.devopsschool.com/blog/wp-content/uploads/2023/04/image-9.png)

## Step 3 – Download installer script on Rocky Linux 8 Nodes

All the Rocky Linux 8 nodes intended for this use need to be configured with the RKE2 repositories that provide the required packages. Instal curl tool on your system:

```
sudo yum -y install curl vim wget
```

With curl download the script used to install RKE2 server on your Rocky Linux 8 servers.

```
curl -sfL https://get.rke2.io --output install.sh
```

Make the script executable:

```
chmod +x install.sh
```

To see script usage options run:

```
less ./install.sh 
```

Once added, you can install and configure both the RKE2 server and agent on the desired nodes.

## Step 4 – Set up the First Server Node (Master Node)

Install RKE2 server:

```
sudo INSTALL_RKE2_TYPE=server ./install.sh
```

Expected output:

```
[INFO]  finding release for channel stable
[INFO]  using 1.23 series from channel stable
Rocky Linux 8 - AppStream                                                                                                                                              19 kB/s | 4.8 kB     00:00
Rocky Linux 8 - AppStream                                                                                                                                              11 MB/s | 9.6 MB     00:00
Rocky Linux 8 - BaseOS                                                                                                                                                 18 kB/s | 4.3 kB     00:00
Rocky Linux 8 - BaseOS                                                                                                                                                 11 MB/s | 6.7 MB     00:00
Rocky Linux 8 - Extras                                                                                                                                                 13 kB/s | 3.5 kB     00:00
Rocky Linux 8 - Extras                                                                                                                                                 41 kB/s |  11 kB     00:00
Rancher RKE2 Common (stable)                                                                                                                                          1.7 kB/s | 1.7 kB     00:00
Rancher RKE2 1.23 (stable)                                                                                                                                            4.8 kB/s | 4.6 kB     00:00
Dependencies resolved.
======================================================================================================================================================================================================
.......

Transaction Summary
======================================================================================================================================================================================================
Install  5 Packages

Total download size: 34 M
Installed size: 166 M
Downloading Packages:
.....
```

Once installed, you need to create a config file manually. The config file contains the `tls-san`parameter which avoids certificate errors with the fixed registration address.

The config file can be created with the command:

```
sudo vim /etc/rancher/rke2/config.yaml
```

Add the below lines to the file replacing where required.

```
write-kubeconfig-mode: "0644"
tls-san:
  - rke.computingforgeeks.com
  - 192.168.205.9
```

Replace ==rke.computingforgeeks.com== with your fixed registration address and ==192.168.205.9== with its IP address.

Save the file and start the service;

```
sudo systemctl start rke2-server
sudo systemctl enable rke2-server
```

Confirm status of the service after starting it:

![](https://www.devopsschool.com/blog/wp-content/uploads/2023/04/image-10.png)

![](https://www.devopsschool.com/blog/wp-content/uploads/2023/04/image-11.png)

![](https://www.devopsschool.com/blog/wp-content/uploads/2023/04/image-12.png)

![](https://www.devopsschool.com/blog/wp-content/uploads/2023/04/image-13.png)

![](https://www.devopsschool.com/blog/wp-content/uploads/2023/04/image-14.png)

![](https://www.devopsschool.com/blog/wp-content/uploads/2023/04/image-15.png)

## Step 7 – Deploy an Application.

Once the above configurations have been made, deploy and application on your cluster. For this guide, we will deploy a demo Nginx application.

```
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 2 
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
EOF
```

Check if the pod is up:

```
$ kubectl get pods
NAME                               READY   STATUS    RESTARTS   AGE
nginx-deployment-cc7df4f8f-frv65   1/1     Running   0          13s
nginx-deployment-cc7df4f8f-l9xdb   1/1     Running   0          13s
```

Now expose the service:

```
$ kubectl expose deployment nginx-deployment --type=NodePort --port=80
service/nginx-deployment exposed
```

Obtain the port to which the service has been exposed:

```
$ kubectl get svc
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes         ClusterIP   10.43.0.1       <none>        443/TCP          85m
nginx-deployment   NodePort    10.43.135.164   <none>        80:31042/TCP     2s
```

In my case, the service has been exposed to port **31042**. Access the application using any controller or worker node IP address with the syntax [http://IP_Address:31042](http://ip_address:31042/)