
pipeline {
    agent any

    environment {
        APP_NAME = 'jenkins-cicd-app'
        IMAGE_NAME = 'jenkins-cicd-python'
        IMAGE_TAG = '1.0.0'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Source code is checked out.'
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

        stage('Deploy Application') {
            steps {
                sh '''
                    docker rm -f ${APP_NAME} || true

                    docker run -d \
                      --name ${APP_NAME} \
                      --restart unless-stopped \
                      -p 5000:5000 \
                      ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    for i in $(seq 1 15); do
                        if curl -fsS \
                          http://localhost:5000/health; then
                            echo "Health check passed."
                            exit 0
                        fi
                        sleep 2
                    done

                    echo "Health check failed."
                    docker logs ${APP_NAME} || true
                    exit 1
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
