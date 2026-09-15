pipeline {
    agent any
    environment {
        APP_NAME = "overthink-engine"
        REGISTRY = "docker.io/sarvesh30"
        IMAGE_TAG = "v${BUILD_NUMBER}"
    }
    stages {
        stage('Checkout & Lint') {
            steps {
                echo 'Checking out source repository...'
                sh 'python -m py_compile src/engine/main.py'
            }
        }
        stage('Build Image') {
            steps {
                echo "Building container image ${REGISTRY}/${APP_NAME}:${IMAGE_TAG}..."
                sh "podman build -t ${REGISTRY}/${APP_NAME}:${IMAGE_TAG} -f src/engine/Dockerfile src/engine/"
            }
        }
        stage('Push to Registry') {
            steps {
                echo "Pushing image to container registry..."
                sh "podman push ${REGISTRY}/${APP_NAME}:${IMAGE_TAG}"
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                echo 'Automating manifest application to Kubernetes cluster...'
                sh "sed -i 's|image: .*|image: ${REGISTRY}/${APP_NAME}:${IMAGE_TAG}|' k8s/deployment.yaml"
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl rollout status deployment/overthink-engine --timeout=60s'
            }
        }
    }
    post {
        success {
            echo 'Continuous Deployment pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Triggering automatic rollback...'
            sh 'kubectl rollout undo deployment/overthink-engine'
        }
    }
}
