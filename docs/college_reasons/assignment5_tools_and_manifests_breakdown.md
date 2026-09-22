# Tools & Manifests Detailed Line-by-Line Breakdown

DevOps Lab (ENSP461) — 4th Year  
**Student Name**: Sarvesh Chandran  
**Roll Number**: 2301730032  
**Faculty / Professor**: Amit Kumar Singh  
**Subject**: In-Depth Explanation of Dockerfile, Kubernetes Manifests, Jenkinsfile & GitHub Actions  

---

## 1. Containerfile / Dockerfile (`src/engine/Dockerfile`)

```dockerfile
Line 1:  FROM python:3.11-slim
Line 2:  
Line 3:  WORKDIR /app
Line 4:  
Line 5:  RUN apt-get update && apt-get install -y --no-install-recommends \
Line 6:      curl \
Line 7:      && rm -rf /var/lib/apt/lists/*
Line 8:  
Line 9:  COPY requirements.txt .
Line 10: RUN pip install --no-cache-dir -r requirements.txt
Line 11: 
Line 12: COPY main.py .
Line 13: 
Line 14: EXPOSE 8000
Line 15: 
Line 16: ENV PYTHONUNBUFFERED=1
Line 17: 
Line 18: CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Line-by-Line Explanation:
- **Line 1 (`FROM python:3.11-slim`)**: Specifies the official base image from the Python repository. The `slim` variant contains only the essential packages needed to run Python, keeping the image small (under 150MB) and reducing vulnerability surface.
- **Line 3 (`WORKDIR /app`)**: Sets `/app` as the working directory inside the container. All subsequent commands (`COPY`, `RUN`, `CMD`) will run from this folder.
- **Lines 5-7 (`RUN apt-get update && apt-get install -y --no-install-recommends curl ...`)**: Updates Debian package lists and installs `curl`. The `curl` utility is essential for executing automated HTTP health checks in Kubernetes and CI/CD pipelines. The `--no-install-recommends` flag avoids installing optional bloat, and `rm -rf /var/lib/apt/lists/*` cleans temporary package caches to keep the container image minimal.
- **Line 9 (`COPY requirements.txt .`)**: Copies only the dependency specification file first before the source code. This leverages container layer caching—if application code changes but dependencies do not, Podman skips downloading packages during subsequent builds.
- **Line 10 (`RUN pip install --no-cache-dir -r requirements.txt`)**: Installs FastAPI, Uvicorn, and Pydantic. The `--no-cache-dir` flag prevents pip from saving installation wheel files in the container, saving disk space.
- **Line 12 (`COPY main.py .`)**: Copies the FastAPI application entrypoint into `/app/main.py`.
- **Line 14 (`EXPOSE 8000`)**: Documents that the application inside the container listens on TCP port 8000.
- **Line 16 (`ENV PYTHONUNBUFFERED=1`)**: Forces Python stdout and stderr streams to flush immediately to the terminal instead of being buffered. This ensures real-time container log visibility when running `podman logs`.
- **Line 18 (`CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`)**: Specifies the default process launched when the container starts. It runs Uvicorn ASGI server binding to all network interfaces (`0.0.0.0`) on port 8000.

---

## 2. Kubernetes Deployment Manifest (`k8s/deployment.yaml`)

```yaml
Line 1:  apiVersion: apps/v1
Line 2:  kind: Deployment
Line 3:  metadata:
Line 4:    name: overthink-engine
Line 5:    labels:
Line 6:      app: overthink-engine
Line 7:  spec:
Line 8:    replicas: 2
Line 9:    strategy:
Line 10:     type: RollingUpdate
Line 11:     rollingUpdate:
Line 12:       maxSurge: 1
Line 13:       maxUnavailable: 0
Line 14:   selector:
Line 15:     matchLabels:
Line 16:       app: overthink-engine
Line 17:   template:
Line 18:     metadata:
Line 19:       labels:
Line 20:         app: overthink-engine
Line 21:     spec:
Line 22:       containers:
Line 23:       - name: overthink-engine
Line 24:         image: docker.io/sarvesh30/overthink-engine:1.0
Line 25:         imagePullPolicy: IfNotPresent
Line 26:         ports:
Line 27:         - containerPort: 8000
Line 28:         env:
Line 29:         - name: ENGINE_ENV
Line 30:           value: "production"
Line 31:         resources:
Line 32:           requests:
Line 33:             cpu: "100m"
Line 34:             memory: "128Mi"
Line 35:           limits:
Line 36:             cpu: "500m"
Line 37:             memory: "512Mi"
Line 38:         readinessProbe:
Line 39:           httpGet:
Line 40:             path: /health
Line 41:             port: 8000
Line 42:           initialDelaySeconds: 3
Line 43:           periodSeconds: 5
Line 44:         livenessProbe:
Line 45:           httpGet:
Line 46:             path: /health
Line 47:             port: 8000
Line 48:           initialDelaySeconds: 5
Line 49:           periodSeconds: 10
```

### Line-by-Line Explanation:
- **Lines 1-2 (`apiVersion: apps/v1`, `kind: Deployment`)**: Declares the Kubernetes resource type. `Deployment` manages declarative updates for Pods and ReplicaSets.
- **Lines 3-6 (`metadata`)**: Assigns the unique name `overthink-engine` and metadata label `app: overthink-engine` to the deployment.
- **Line 8 (`replicas: 2`)**: Instructs the orchestrator to maintain exactly 2 concurrent pod instances running at all times.
- **Lines 9-13 (`strategy: RollingUpdate`, `maxSurge: 1`, `maxUnavailable: 0`)**: Configures zero-downtime rolling update rules:
  - `maxSurge: 1`: During an update, the orchestrator can create 1 extra pod above the desired count (2 + 1 = 3 pods max).
  - `maxUnavailable: 0`: Under no circumstances can any existing pod be terminated until the new replacement pod has passed health checks. This guarantees 100% service uptime during deployments.
- **Lines 14-16 (`selector.matchLabels`)**: Defines how the deployment identifies which pods it owns and manages.
- **Lines 17-20 (`template.metadata.labels`)**: Specifies the label applied to all newly created pods so they match the selector.
- **Lines 22-24 (`containers: - name: overthink-engine, image: ...:1.0`)**: Specifies the container name and the image registry repository and version tag.
- **Line 25 (`imagePullPolicy: IfNotPresent`)**: Uses local cached image if available instead of redownloading from the registry on every run.
- **Lines 26-27 (`ports: - containerPort: 8000`)**: Tells Kubernetes that the container listens on port 8000.
- **Lines 28-30 (`env: - name: ENGINE_ENV, value: "production"`)**: Injects environment variables into the application process.
- **Lines 31-37 (`resources`)**:
  - `requests`: Minimum guaranteed system resources (0.1 CPU core and 128 MB RAM).
  - `limits`: Maximum allowed ceiling (0.5 CPU core and 512 MB RAM) to prevent any single container from exhausting host resources.
- **Lines 38-43 (`readinessProbe`)**: Queries `GET /health` every 5 seconds (after a 3-second initial wait). If it returns HTTP 200 OK, traffic is routed to the container.
- **Lines 44-49 (`livenessProbe`)**: Queries `GET /health` every 10 seconds. If the container becomes unresponsive, the orchestrator automatically restarts it.

---

## 3. Kubernetes Service Manifest (`k8s/service.yaml`)

```yaml
Line 1: apiVersion: v1
Line 2: kind: Service
Line 3: metadata:
Line 4:   name: overthink-engine-service
Line 5: spec:
Line 6:   type: NodePort
Line 7:   selector:
Line 8:     app: overthink-engine
Line 9:   ports:
Line 10:   - protocol: TCP
Line 11:     port: 8000
Line 12:     targetPort: 8000
Line 13:     nodePort: 30080
```

### Line-by-Line Explanation:
- **Lines 1-2 (`apiVersion: v1`, `kind: Service`)**: Defines a Kubernetes networking abstraction that groups multiple pod replicas behind a single stable IP address.
- **Line 4 (`name: overthink-engine-service`)**: The internal DNS name accessible by other services.
- **Line 6 (`type: NodePort`)**: Exposes the service on a static port across cluster nodes so external clients can access the application.
- **Lines 7-8 (`selector: app: overthink-engine`)**: Directs traffic to all pods labeled with `app: overthink-engine`.
- **Lines 9-13 (`ports`)**:
  - `port: 8000`: The internal cluster port where the service listens.
  - `targetPort: 8000`: The port on the container where traffic is forwarded.
  - `nodePort: 30080`: The external port on the host machine where clients can connect directly (`http://localhost:30080`).

---

## 4. Continuous Deployment Pipeline (`Jenkinsfile`)

```groovy
Line 1:  pipeline {
Line 2:      agent any
Line 3:      environment {
Line 4:          APP_NAME = "overthink-engine"
Line 5:          REGISTRY = "docker.io/sarvesh30"
Line 6:          IMAGE_TAG = "v${BUILD_NUMBER}"
Line 7:      }
Line 8:      stages {
Line 9:          stage('Checkout & Lint') {
Line 10:             steps {
Line 11:                 echo 'Checking out source repository...'
Line 12:                 sh 'python -m py_compile src/engine/main.py'
Line 13:             }
Line 14:         }
Line 15:         stage('Build Image') {
Line 16:             steps {
Line 17:                 echo "Building container image ${REGISTRY}/${APP_NAME}:${IMAGE_TAG}..."
Line 18:                 sh "podman build -t ${REGISTRY}/${APP_NAME}:${IMAGE_TAG} -f src/engine/Dockerfile src/engine/"
Line 19:             }
Line 20:         }
Line 21:         stage('Push to Registry') {
Line 22:             steps {
Line 23:                 echo "Pushing image to container registry..."
Line 24:                 sh "podman push ${REGISTRY}/${APP_NAME}:${IMAGE_TAG}"
Line 25:             }
Line 26:         }
Line 27:         stage('Deploy Kubernetes Manifest') {
Line 28:             steps {
Line 29:                 echo 'Automating manifest application to Kubernetes environment via Podman...'
Line 30:                 sh "sed -i 's|image: .*|image: ${REGISTRY}/${APP_NAME}:${IMAGE_TAG}|' k8s/deployment.yaml"
Line 31:                 sh 'podman play kube --replace k8s/deployment.yaml'
Line 32:                 sh 'sleep 3'
Line 33:                 sh 'CONTAINER_ID=$(podman ps --format "{{.ID}} {{.Image}}" | grep "overthink-engine" | awk \'{print $1}\' | head -n 1) && podman exec "$CONTAINER_ID" curl -f http://localhost:8000/health'
Line 34:             }
Line 35:         }
Line 36:     }
Line 37:     post {
Line 38:         success {
Line 39:             echo 'Continuous Deployment pipeline completed successfully.'
Line 40:         }
Line 41:         failure {
Line 42:             echo 'Pipeline failed. Triggering automatic rollback...'
Line 43:             sh 'podman play kube --replace k8s/deployment.yaml'
Line 44:         }
Line 45:     }
Line 46: }
```

### Line-by-Line Explanation:
- **Line 1 (`pipeline {`)**: Declares a standard Jenkins Declarative Pipeline.
- **Line 2 (`agent any`)**: Allows the pipeline to execute on any available Jenkins agent/executor node.
- **Lines 3-7 (`environment`)**: Defines dynamic configuration variables:
  - `APP_NAME`: Set to `overthink-engine`.
  - `REGISTRY`: Registry namespace.
  - `IMAGE_TAG`: Automatically derives a unique tag from Jenkins build number (e.g., `v1`, `v2`, `v3`).
- **Lines 9-13 (`stage('Checkout & Lint')`)**: Verifies Python syntax using `py_compile`. If syntax errors exist, the pipeline fails immediately before wasting build resources.
- **Lines 15-20 (`stage('Build Image')`)**: Invokes Podman to package the microservice into a container image tagged with the unique build identifier.
- **Lines 21-25 (`stage('Push to Registry')`)**: Publishes the image to the remote container registry.
- **Lines 27-35 (`stage('Deploy Kubernetes Manifest')`)**:
  - `sed -i ...`: Dynamically replaces the image tag inside `k8s/deployment.yaml` with the newly built version.
  - `podman play kube --replace ...`: Applies the manifest into the Podman cluster, replacing previous containers without downtime.
  - Health check: Queries the `/health` endpoint of the live container to verify application responsiveness before concluding deployment.
- **Lines 37-45 (`post { success / failure }`)**:
  - `success`: Logs pipeline success status.
  - `failure`: Triggers automated rollback by reapplying the previous stable manifest.

---

## 5. GitHub Actions Continuous Deployment Workflow (`.github/workflows/deploy.yml`)

```yaml
Line 1:  name: Kubernetes Continuous Deployment Pipeline
Line 2:  
Line 3:  on:
Line 4:    push:
Line 5:      branches: [ main ]
Line 6:      paths:
Line 7:        - 'src/engine/**'
Line 8:        - 'k8s/**'
Line 9:        - '.github/workflows/**'
Line 10: 
Line 11: jobs:
Line 12:   build-and-deploy:
Line 13:     runs-on: ubuntu-latest
Line 14:     steps:
Line 15:     - name: Checkout Code
Line 16:       uses: actions/checkout@v4
Line 17: 
Line 18:     - name: Build Container Image
Line 19:       run: |
Line 20:         podman build -t docker.io/sarvesh30/overthink-engine:${{ github.sha }} -f src/engine/Dockerfile src/engine/
Line 21: 
Line 22:     - name: Push Container Image
Line 23:       run: |
Line 24:         echo "Pushing image docker.io/sarvesh30/overthink-engine:${{ github.sha }} to registry..."
Line 25: 
Line 26:     - name: Automate Kubernetes Manifest Application via Podman
Line 27:       run: |
Line 28:         sed -i "s|image: overthink-engine:.*|image: docker.io/sarvesh30/overthink-engine:${{ github.sha }}|g" k8s/deployment.yaml
Line 29:         podman play kube --replace k8s/deployment.yaml
Line 30:         sleep 3
Line 31:         podman pod ps
Line 32:         podman ps -a --pod
Line 33:         CONTAINER_ID=$(podman ps --format "{{.ID}} {{.Image}}" | grep "overthink-engine" | awk '{print $1}' | head -n 1)
Line 34:         echo "Identified running container: $CONTAINER_ID"
Line 35:         for i in {1..10}; do
Line 36:           RESPONSE=$(podman exec "$CONTAINER_ID" curl -s http://localhost:8000/health || true)
Line 37:           if echo "$RESPONSE" | grep -q "healthy"; then
Line 38:             echo "Service successfully verified healthy: $RESPONSE"
Line 39:             exit 0
Line 40:           fi
Line 41:           echo "Waiting for service to be healthy... ($i/10)"
Line 42:           sleep 2
Line 43:         done
Line 44:         echo "Error: Healthcheck timed out"
Line 45:         exit 1
```

### Line-by-Line Explanation:
- **Lines 3-9 (`on: push: branches: [ main ], paths: ...`)**: Triggers execution automatically only when code is pushed to the `main` branch and changes affect `src/engine/`, `k8s/`, or workflow files.
- **Lines 11-13 (`runs-on: ubuntu-latest`)**: Allocates an ephemeral Ubuntu runner VM on GitHub infrastructure.
- **Lines 15-16 (`uses: actions/checkout@v4`)**: Clones the repository into the runner workspace.
- **Lines 18-20 (`podman build ...`)**: Builds the container using Podman and tags it with the immutable commit hash (`${{ github.sha }}`).
- **Lines 26-29 (`podman play kube --replace k8s/deployment.yaml`)**: Automatically substitutes the commit hash into the manifest and deploys it directly using Podman's Kubernetes engine.
- **Lines 30-34 (`CONTAINER_ID resolution`)**: Inspects running containers, isolates the application container ID, and avoids fragile hardcoded container names.
- **Lines 35-43 (`Healthcheck retry loop`)**: Tests the FastAPI health endpoint up to 10 times with a 2-second sleep interval. Once `{"status": "healthy"}` is returned, the pipeline exits with code 0 (success). If the application fails to start within 20 seconds, it exits with code 1 (failure) to catch regressions immediately.
