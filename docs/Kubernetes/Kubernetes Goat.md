<span style="color:#4caf50;"><b>Created:</b> 2025-08-05</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-08-05</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>


✨ The Kubernetes Goat is designed to be an intentionally vulnerable cluster environment to learn and practice Kubernetes security 🚀 https://github.com/gowseshaik/kubernetes-goat

🙌 Refer to **[https://madhuakula.com/kubernetes-goat](https://madhuakula.com/kubernetes-goat)** for the guide 📖

 [![Netlify Status](https://camo.githubusercontent.com/8a88ff8a8416f941452ef135bcfaea3d8722eda45b56b7e8f4cc40ee1a6af737/68747470733a2f2f6170692e6e65746c6966792e636f6d2f6170692f76312f6261646765732f65353339396265332d396334372d343535372d623233372d3965366338396636636164612f6465706c6f792d737461747573)](https://app.netlify.com/sites/kubernetes-goat/deploys) [![License: MIT](https://camo.githubusercontent.com/cce5a2a14b0faab422e0bfcdc074afb46089831a0bf5930a7d8af3f31b98f847/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4d49542d626c75652e737667)](https://github.com/madhuakula/kubernetes-goat/blob/master/LICENSE) [![GitHub release](https://camo.githubusercontent.com/17ca074f486af3c07fcabc3aa18feb8112e0e26218d7a5800d9b81729c4ca93c/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f72656c656173652f6d61646875616b756c612f6b756265726e657465732d676f61742e737667)](https://github.com/madhuakula/kubernetes-goat/releases/latest) [![Github Stars](https://camo.githubusercontent.com/36d4bb0ecccb8e8a4a0c5904cfca75a376253417bd505809cba978d8ee696fde/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f73746172732f6d61646875616b756c612f6b756265726e657465732d676f6174)](https://github.com/madhuakula/kubernetes-goat/stargazers) [![PRs Welcome](https://camo.githubusercontent.com/d88d8d77fa79e828eea397f75a1ebd114d13488aeec4747477ffbd2274de95ed/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5052732d77656c636f6d652d627269676874677265656e2e737667)](https://github.com/madhuakula/kubernetes-goat/pulls) [![Docker Pulls Kubernetes Goat](https://camo.githubusercontent.com/4fbca184c4ef8be299666f4998580693cba711db4fb4e53144c9c0d345f7f747/68747470733a2f2f696d672e736869656c64732e696f2f646f636b65722f70756c6c732f6d61646875616b756c612f6b38732d676f61742d73797374656d2d6d6f6e69746f72)](https://hub.docker.com/r/madhuakula/k8s-goat-system-monitor) [![Twitter](https://camo.githubusercontent.com/fcdcfd1aecb91d7fd91c2dbf7da042103c2b7d61bfdebab98ce50249762859e1/68747470733a2f2f696d672e736869656c64732e696f2f747769747465722f75726c3f75726c3d68747470733a2f2f6769746875622e636f6d2f6d61646875616b756c612f6b756265726e657465732d676f6174)](https://twitter.com/intent/tweet/?text=Kubernetes%20Goat,%20an%20intentionally%20vulnerable%20by%20design%20training%20platform%20to%20learn%20%23Kubernetes%20Security%20by%20%40madhuakula.%20Check%20it%20out%20&url=https://github.com/madhuakula/kubernetes-goat)[![Discord](https://camo.githubusercontent.com/9d30bb47d4d530212eea8dcdcbfdaf9fb0e8e6de3cc93439171d5f62513eb37a/68747470733a2f2f696d672e736869656c64732e696f2f646973636f72642f3937363530333836343236383330383538303f636f6c6f723d396366266c6162656c3d446973636f7264266c6f676f3d646973636f7264266c6f676f436f6c6f723d7768697465)](https://rebrand.ly/Kubernetes-Goat/)

[![Kubernetes Goat Home](https://github.com/gowseshaik/kubernetes-goat/raw/master/kubernetes-goat-home.png)](https://madhuakula.com/kubernetes-goat)
## 🧰 Setting up Kubernetes Goat

- Ensure you have admin access to the Kubernetes cluster and installed `kubectl`. Refer to the [docs for installation](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- Ensure you have the `helm` package manager installed. Refer to the [docs for installation](https://helm.sh/docs/intro/install)
- To set up the Kubernetes Goat resources in your cluster, run the following commands:

```shell
git clone https://github.com/madhuakula/kubernetes-goat.git
cd kubernetes-goat
chmod +x setup-kubernetes-goat.sh
bash setup-kubernetes-goat.sh
```

- Ensure the pods are running before running the access script

```shell
kubectl get pods
```

[![all pods running in kubectl get pods](https://github.com/gowseshaik/kubernetes-goat/raw/master/guide/docs/scenarios/images/kubectl-get-pods.png)](https://github.com/gowseshaik/kubernetes-goat/blob/master/guide/docs/scenarios/images/kubectl-get-pods.png)

- Access Kubernetes Goat by exposing the resources to the local system (port-forward) by the following command:

```shell
bash access-kubernetes-goat.sh
```

- Then navigate to [`http://127.0.0.1:1234`](http://127.0.0.1:1234/)

> Refer to [https://madhuakula.com/kubernetes-goat/docs/how-to-run](https://madhuakula.com/kubernetes-goat/docs/how-to-run) for setting up Kubernetes Goat in various environments like GKE, EKS, AKS, K3S, KIND, etc.

## 🏆 Scenarios

1. Sensitive keys in codebases
2. DIND (docker-in-docker) exploitation
3. SSRF in the Kubernetes (K8S) world
4. Container escape to the host system
5. Docker CIS benchmarks analysis
6. Kubernetes CIS benchmarks analysis
7. Attacking private registry
8. NodePort exposed services
9. Helm v2 tiller to PwN the cluster - [Deprecated]
10. Analyzing crypto miner container
11. Kubernetes namespaces bypass
12. Gaining environment information
13. DoS the Memory/CPU resources
14. Hacker container preview
15. Hidden in layers
16. RBAC least privileges misconfiguration
17. KubeAudit - Audit Kubernetes clusters
18. Falco - Runtime security monitoring & detection
19. Popeye - A Kubernetes cluster sanitizer
20. Secure network boundaries using NSP
21. Cilium Tetragon - eBPF-based Security Observability and Runtime Enforcement
22. Securing Kubernetes Clusters using Kyverno Policy Engine

## 📖 Documentation Guide

Here is the detailed step by step guide for learning and using Kubernetes Goat 🎉: [documentation guide](https://madhuakula.com/kubernetes-goat)

[![Kubernetes Goat Documentation Guide](https://github.com/gowseshaik/kubernetes-goat/raw/master/kubernetes-goat-docs.png)](https://madhuakula.com/kubernetes-goat)
**Reference: [https://madhuakula.com/kubernetes-goat](https://madhuakula.com/kubernetes-goat)**
## ⚠️ Disclaimer

> Kubernetes Goat has intentionally created vulnerabilities, applications, and configurations to attack and gain access to your cluster and workloads. Please **DO NOT** run this alongside your production environments and infrastructure. We highly recommend running this in a safe and isolated (contained) environment.

> Kubernetes Goat is used for educational purposes only. Do not test or apply these attacks on any systems without permission. Kubernetes Goat comes with absolutely no warranties, by using it you take full responsibility for all outcomes.