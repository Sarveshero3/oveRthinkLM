# 0001. Kubernetes-Syntax Manifests Orchestrated via Podman Play Kube

The ENSP461 capstone requires Kubernetes orchestration, but running a full Kubernetes cluster (minikube/k3s) exceeds the development machine's lean local resource constraints. We decide to author authentic Kubernetes-syntax YAML manifests (`apps/v1`, `v1`) and orchestrate them locally using `podman play kube`. The manifests remain 100% portable to any standard K8s cluster without modification.
