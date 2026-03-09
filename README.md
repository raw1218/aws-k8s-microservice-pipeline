# Kubernetes Microservice CI/CD Pipeline

This project demonstrates a **containerized microservice deployed to Kubernetes with an automated Docker build pipeline**.

The API itself is intentionally simple. The main purpose of the project is to demonstrate:

- Docker containerization
- Kubernetes deployments and services
- Local Kubernetes clusters with **kind**
- CI/CD pipelines using **GitHub Actions**
- Automatic Docker image builds and pushes

---


# API Endpoints

| Endpoint | Description |
|---------|-------------|
| `/` | Service status |
| `/health` | Health check |
| `/time` | Current server time |
| `/version` | Version indicator |

Example response:

```json
{
  "message": "Kubernetes microservice running"
}
```

---

# Prerequisites

Install the following tools before running the project.

### Docker
https://docs.docker.com/get-docker/

### kubectl
https://kubernetes.io/docs/tasks/tools/

### kind
https://kind.sigs.k8s.io/

### Git
https://git-scm.com/

---

# Running the Project Locally

## 1. Clone the repository

```
git clone https://github.com/YOUR_USERNAME/aws-k8s-microservice-pipeline.git
cd aws-k8s-microservice-pipeline
```

---

## 2. Create a Kubernetes cluster

```
kind create cluster --config kind-config.yaml
```

Verify the cluster:

```
kubectl get nodes
```

Expected output:

```
NAME                                 STATUS   ROLES           AGE   VERSION
microservice-cluster-control-plane   Ready    control-plane   ...
```

---

## 3. Deploy the application

Apply the Kubernetes manifests:

```
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Verify the pods are running:

```
kubectl get pods
```

Expected output:

```
microservice-deployment-xxxxx   Running
```

---

## 4. Access the API

Forward the Kubernetes service to localhost for local testing:

```
kubectl port-forward service/microservice-service 8000:8000
```

The API will now be available at:

```
http://localhost:8000
```

---

# Testing the API

Example endpoints:

```
http://localhost:8000/
http://localhost:8000/health
http://localhost:8000/time
http://localhost:8000/version
```

Example response:

```json
{
  "status": "ok"
}
```

---

# Updating the Application

If the API code changes:

1. Push the changes to GitHub
2. GitHub Actions automatically builds a new Docker image
3. The image is pushed to Docker Hub

To update the running Kubernetes pods:

```
kubectl rollout restart deployment microservice-deployment
```

This forces Kubernetes to pull the updated image.
