
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'jenkins-cicd-python'
        IMAGE_TAG = '2.0'
        APP_NAME = 'jenkins-cicd-app'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '.venv/bin/pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                    trivy image \
                      --severity HIGH,CRITICAL \
                      --exit-code 1 \
                      --no-progress \
                      ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Load Image into Minikube') {
            steps {
                sh '''
                    minikube image load ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f kubernetes/namespace.yaml

                    kubectl apply -f kubernetes/deployment.yaml
                    kubectl apply -f kubernetes/service.yaml
                    kubectl apply -f kubernetes/hpa.yaml

                    kubectl rollout status \
                      deployment/${APP_NAME} \
                      --timeout=180s
                '''
            }
        }

        stage('Deploy Monitoring') {
            steps {
                sh '''
                    kubectl apply -f kubernetes/prometheus-rbac.yaml
                    kubectl apply -f kubernetes/prometheus-config.yaml
                    kubectl apply -f kubernetes/prometheus-deployment.yaml

                    kubectl apply -f kubernetes/grafana-datasource.yaml
                    kubectl apply -f kubernetes/grafana-deployment.yaml
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    kubectl get deployments
                    kubectl get pods
                    kubectl get services
                    kubectl get pods -n monitoring
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }

        always {
            echo 'Pipeline execution finished.'
        }
    }
}
