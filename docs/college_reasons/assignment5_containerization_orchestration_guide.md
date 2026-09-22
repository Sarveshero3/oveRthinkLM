# Assignment 5: Containerization & Orchestration Comprehensive Guide

DevOps Lab (ENSP461) — 4th Year  
**Student Name**: Sarvesh Chandran  
**Roll Number**: 2301730032  
**Faculty / Professor**: Amit Kumar Singh  
**Target Application**: `overthink-engine` (FastAPI Microservice)  
**Primary Tool**: Podman 5.8.3  

---

## 1. What Is This Assignment About?

This assignment covers the full lifecycle of **Containerization** and **Kubernetes Orchestration** using modern container tooling:
1. **Containerization**: Packaging a Python FastAPI backend service (`overthink-engine`) along with all its system dependencies, libraries, and runtime environment into an immutable, portable OCI image.
2. **Orchestration with Podman**: Using Podman's native Kubernetes interpreter (`podman play kube`) to deploy, scale, update, and manage the application using standard Kubernetes manifests (`k8s/deployment.yaml`, `k8s/service.yaml`) without requiring a heavyweight Kubernetes cluster.
3. **High Availability Strategies**:
   - **Dynamic Replica Scaling**: Expanding replicas under traffic load and shrinking during idle periods.
   - **Zero-Downtime Rolling Updates**: Replacing older image versions with newer versions while ensuring user requests are never dropped.
   - **Automated Rollback**: Restoring the previous working state if a new release exhibits issues.

---

## 2. Why Are We Doing It This Way?

### Why Containerization?
In traditional software development, running code across different developer machines or servers frequently suffers from the *"It works on my machine"* problem. Differences in OS versions, Python versions, missing libraries, or background services cause unpredictable bugs. Containerization packages the exact OS filesystem layer, Python runtime, and dependencies together into a standardized image, guaranteeing identical execution anywhere.

### Why Podman Instead of Docker?
In our laboratory and production environment, we exclusively use **Podman**:
1. **Daemonless Architecture**: Docker requires a continuously running background root daemon (`dockerd`). If the daemon crashes, all containers go down. Podman operates on a fork-exec model using `conmon` (container monitor). Each container runs as a direct child process of the user command, eliminating a single point of failure.
2. **Rootless by Design**: Docker historically requires root privileges to interact with the Docker socket, presenting significant security risks. Podman runs completely in user space (rootless mode) using user namespaces, preventing container escape exploits from gaining root access to the host.
3. **Native Kubernetes Orchestration (`podman play kube`)**: Standard Docker cannot read or run Kubernetes manifests natively without installing external tools like Minikube or Kind. Podman has first-class built-in support for Kubernetes YAML syntax. Running `podman play kube k8s/deployment.yaml` creates native pods and containers directly.
4. **Standard OCI Compliance**: Podman adheres to Open Container Initiative (OCI) specifications, meaning images built with Podman are 100% compatible with any standard container registry.

---

## 3. How Does the Architecture Work?

### Component Architecture
```
[ Developer Workstation / CI Runner ]
                 │
                 ▼
        [ Git Repository ]
                 │
                 ▼
   [ Container Image Build ] (Podman 5.8.3)
   Image: overthink-engine:1.0 / 2.0 / v3
                 │
                 ▼
   [ Podman Kube Orchestrator ] (podman play kube)
                 │
                 ▼
     ┌──────────────────────────────────────────────┐
     │            Pod: overthink-engine-pod         │
     │  ┌────────────────────────────────────────┐  │
     │  │  Infra Container (Pause: 8000->8000)   │  │
     │  └───────────────────┬────────────────────┘  │
     │                      │ (Shared Network / IPC)│
     │  ┌───────────────────┴────────────────────┐  │
     │  │ Container: overthink-engine-replica-1  │  │
     │  │ (FastAPI App running on port 8000)     │  │
     │  └────────────────────────────────────────┘  │
     │  ┌────────────────────────────────────────┐  │
     │  │ Container: overthink-engine-replica-2  │  │
     │  │ (FastAPI App running on port 8000)     │  │
     │  └────────────────────────────────────────┘  │
     └──────────────────────────────────────────────┘
```

### Key Concepts Explained for Beginners:
- **Pod**: The smallest deployable unit in Kubernetes. In Podman, a pod is a group of one or more containers that share the same network namespace, IP address, and port mapping.
- **Infra (Pause) Container**: The foundation of a pod. It holds the network ports and IPC namespace open so application containers inside the pod can talk to each other over `localhost`.
- **Readiness Probe**: A health check query that tells the orchestrator whether the container is ready to accept user requests. Podman monitors this before routing traffic to new pods.
- **Liveness Probe**: A periodic check verifying that the container application is still healthy. If it hangs or deadlocks, the orchestrator restarts the container.

---

## 4. Step-by-Step Execution Workflow

### Step 1: Container Build
- The service is packaged using `podman build -t overthink-engine:1.0 -f src/engine/Dockerfile src/engine/`.
- Podman executes layer by layer, caching unchanged dependencies to minimize build time.

### Step 2: Deployment Application
- Executing `podman play kube k8s/deployment.yaml` reads the Kubernetes Deployment specification.
- Podman creates the pod, starts the infra pause container, assigns port `8000:8000`, and spins up the requested 2 replicas.

### Step 3: Scaling Experiments
- **Scale Up (2 -> 4 replicas)**: `podman play kube --replace k8s/deployment-scale.yaml` updates the pod definition. Podman dynamically launches two additional replica containers to distribute load.
- **Scale Down (4 -> 2 replicas)**: `podman play kube --replace k8s/deployment.yaml` gracefully stops and deletes the two excess containers, reclaiming host memory.

### Step 4: Rolling Update (Zero Downtime)
- Image is bumped to `overthink-engine:2.0` in `k8s/deployment-v2.yaml`.
- Executing `podman play kube --replace k8s/deployment-v2.yaml` initiates the update.
- Podman starts new containers running the version 2.0 image, verifies that their health check endpoints return HTTP 200, and only then retires the older version 1.0 containers.

### Step 5: Rollback Strategy
- If an update encounters regression, running `podman play kube --replace k8s/deployment.yaml` immediately restores the previous stable container image (`version 1.0`).

### Step 6: Resource Cleanup
- Running `podman play kube --down k8s/deployment.yaml` stops all containers, removes the pod, and releases host network ports cleanly.
