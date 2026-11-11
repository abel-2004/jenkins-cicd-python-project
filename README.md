# Python Flask DevOps CI/CD Project

A hands-on DevOps project that demonstrates how to build, test, containerize, scan, deploy, and monitor a Python Flask application using modern DevOps tools.

The project integrates **Linux, Git, GitHub, GitHub Actions, Jenkins, Docker, Kubernetes, Prometheus, and Grafana** into a CI/CD workflow.

## 1. Project Overview

The application is a Python Flask-based DevOps Status API.

It provides:
- A home endpoint displaying application information.
- A health-check endpoint for Kubernetes probes.
- A Prometheus metrics endpoint for monitoring.
- Automated application testing.
- Docker multi-stage image building.
- Container vulnerability scanning using Trivy.
- Kubernetes deployment and scaling.
- Application monitoring using Prometheus and Grafana.

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Linux (Ubuntu/WSL2) | Development environment |
| Git | Version control |
| GitHub | Source code management |
| GitHub Actions | Automated CI |
| Jenkins | CI/CD automation |
| Python | Application development |
| Flask | Web framework |
| Pytest | Application testing |
| Docker | Containerization |
| Docker Multi-stage Build | Optimized container images |
| Trivy | Container vulnerability scanning |
| Kubernetes | Application orchestration |
| Minikube | Local Kubernetes cluster |
| Prometheus | Metrics collection |
| Grafana | Monitoring dashboards |

## 3. Project Architecture

```text
                 Developer
                     |
                     v
                Git / GitHub
                     |
          +----------+----------+
          |                     |
          v                     v
    GitHub Actions            Jenkins
          |                     |
          v                     v
      Run Tests             Checkout Code
          |                     |
          v                     v
     Docker Build           Install Dependencies
                                |
                                v
                            Run Tests
                                |
                                v
                         Docker Image Build
                                |
                                v
                         Trivy Security Scan
                                |
                                v
                         Load Image to Minikube
                                |
                                v
                         Kubernetes Deployment
                                |
                    +-----------+-----------+
                    |                       |
                    v                       v
                Flask API              Monitoring
                    |                       |
                    v                       v
                /metrics               Prometheus
                                            |
                                            v
                                          Grafana
```

## 4. Application Endpoints

The Flask application exposes the following endpoints:

| Endpoint | Description |
|---|---|
| `/` | Application information |
| `/health` | Application health status |
| `/metrics` | Prometheus application metrics |

Example:

```bash
curl http://localhost:5000/
```

Health check:

```bash
curl http://localhost:5000/health
```

Prometheus metrics:

```bash
curl http://localhost:5000/metrics
```

## 5. Prometheus Metrics

The application uses the `prometheus-client` Python library.

Metrics include:

- `app_requests_total` – Total HTTP requests.
- `app_request_duration_seconds` – HTTP request duration.

The metrics endpoint exposes these metrics in Prometheus format.

Example:

```bash
curl http://localhost:5000/metrics
```

## 6. Docker Multi-stage Build

The Dockerfile uses two stages:

### Builder Stage

- Uses Python 3.12 slim.
- Creates a Python virtual environment.
- Installs application dependencies.

### Runtime Stage

- Uses a clean Python 3.12 slim image.
- Copies the virtual environment from the builder stage.
- Copies the Flask application.
- Runs the application using Gunicorn.

Build the Docker image:

```bash
docker build -t jenkins-cicd-python:2.0 .
```

Run the container:

```bash
docker run -d \
  --name jenkins-cicd-app \
  -p 5002:5000 \
  jenkins-cicd-python:2.0
```

Test the application:

```bash
curl http://localhost:5002/health
```

## 7. GitHub Actions CI Pipeline

GitHub Actions automates the CI process.

Workflow file:

```text
.github/workflows/ci.yml
```

The workflow runs when code is pushed to the `main` branch or a pull request targets `main`.

Pipeline stages:

1. Checkout source code.
2. Set up Python 3.12.
3. Install dependencies.
4. Run Pytest tests.
5. Build the Docker image.

The GitHub Actions runner performs the CI process independently of the local Minikube cluster.

## 8. Jenkins CI/CD Pipeline

Jenkins automates the local CI/CD process.

Pipeline file:

```text
Jenkinsfile
```

Pipeline stages:

1. Checkout source code.
2. Create a Python virtual environment.
3. Install dependencies.
4. Run automated tests.
5. Build the Docker image.
6. Scan the image using Trivy.
7. Load the image into Minikube.
8. Deploy the application to Kubernetes.
9. Deploy Prometheus and Grafana.
10. Verify deployments and pods.

Jenkins requires access to Docker, Minikube, kubectl, and Trivy on its build agent.

## 9. Trivy Security Scanning

Trivy is used to scan the Docker image for vulnerabilities.

Example command:

```bash
trivy image \
  --severity HIGH,CRITICAL \
  --exit-code 1 \
  --no-progress \
  jenkins-cicd-python:2.0
```

The pipeline is configured to fail when HIGH or CRITICAL vulnerabilities are found.

## 10. Kubernetes Deployment

The application is deployed to a local Kubernetes cluster using Minikube.

Kubernetes resources include:

- Namespace
- Deployment
- Service
- Horizontal Pod Autoscaler (HPA)

### Deployment

The application Deployment is configured with three replicas.

It includes:
- Container port configuration.
- CPU and memory requests and limits.
- Readiness probes.
- Liveness probes.

### Service

A NodePort Service exposes the application outside the cluster.

### Horizontal Pod Autoscaler

The HPA is configured to:
- Maintain a minimum of 3 replicas.
- Scale up to 6 replicas.
- Target 70% average CPU utilization.

The Kubernetes Metrics Server must be enabled for CPU-based autoscaling.

Enable it in Minikube:

```bash
minikube addons enable metrics-server
```

Check the HPA:

```bash
kubectl get hpa
```

## 11. Prometheus Monitoring

Prometheus runs inside the Kubernetes monitoring namespace.

It uses Kubernetes service discovery to discover the Flask application's Service endpoints.

Prometheus configuration is stored in a ConfigMap.

Monitoring resources include:

- ServiceAccount
- ClusterRole
- ClusterRoleBinding
- ConfigMap
- Prometheus Deployment
- Prometheus Service

Prometheus scrapes application metrics from:

```text
/metrics
```

Default scrape interval:

```yaml
scrape_interval: 15s
```

## 12. Grafana Monitoring

Grafana is deployed inside the Kubernetes monitoring namespace.

Prometheus is configured as the default Grafana data source.

Grafana can be accessed locally using port forwarding:

```bash
kubectl port-forward -n monitoring svc/grafana 3001:3000
```

Open:

```text
http://localhost:3001
```

The example development credentials in the supplied manifest are:

```text
Username: admin
Password: admin123
```

**Security note:** These are demonstration credentials only. Replace them with a Kubernetes Secret or another secure credential-management method before using this project beyond a local learning environment. Do not commit real passwords or secrets.

## 13. Project Structure

```text
jenkins-cicd-python/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── Jenkinsfile
├── README.md
│
├── tests/
│   └── test_app.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
└── kubernetes/
    ├── namespace.yaml
    ├── deployment.yaml
    ├── service.yaml
    ├── hpa.yaml
    ├── prometheus-config.yaml
    ├── prometheus-rbac.yaml
    ├── prometheus-deployment.yaml
    ├── grafana-datasource.yaml
    └── grafana-deployment.yaml
```

## 14. Useful Kubernetes Commands

Check cluster nodes:

```bash
kubectl get nodes
```

Check application pods:

```bash
kubectl get pods
```

Check deployments:

```bash
kubectl get deployments
```

Check services:

```bash
kubectl get services
```

Check monitoring resources:

```bash
kubectl get all -n monitoring
```

Check application logs:

```bash
kubectl logs deployment/jenkins-cicd-app
```

Check HPA:

```bash
kubectl get hpa
```

Check rollout status:

```bash
kubectl rollout status deployment/jenkins-cicd-app
```

## 15. What I Learned

Through this project, I practiced:

- Working with Linux and command-line tools.
- Managing source code using Git and GitHub.
- Creating GitHub Actions CI workflows.
- Building Jenkins declarative pipelines.
- Writing Docker multi-stage builds.
- Running automated tests using Pytest.
- Scanning container images using Trivy.
- Deploying applications to Kubernetes.
- Configuring Deployments, Services, and HPA.
- Exposing application metrics using Prometheus.
- Configuring Grafana with Prometheus as a data source.
- Automating application deployment and verification.

## 16. Future Improvements

Possible improvements include:

- Push Docker images to GitHub Container Registry (GHCR).
- Add Kubernetes rolling-update and rollback automation.
- Create custom Grafana dashboards.
- Add persistent storage for Prometheus and Grafana.
- Store credentials securely using Kubernetes Secrets.
- Add automated integration tests.
- Add alerting using Prometheus Alertmanager.
- Introduce Helm charts for Kubernetes deployment.

## Conclusion

This project demonstrates a practical DevOps workflow covering application development, CI automation, containerization, security scanning, Kubernetes deployment, and monitoring.

It is designed as a local hands-on DevOps learning and portfolio project.
