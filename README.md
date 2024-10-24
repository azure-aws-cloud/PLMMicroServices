## PLM Microservices using Python Full stack
# PLM as enterprise platform has been largely implemented in Java Enterprise
This project attempts to create a standard enterprise microservices based architecture using popular 
frameworks as mentioned below 
```
FASTAPI
Pydantic
SQLAlchemy
```

# Setup 
OS - Mac 10.15 Sequoia, Docker Desktop , Minikube and PostgreSQL DB 14

# Database changes
## Add the following line to the pg_hba.conf
```
host    all             all             0.0.0.0/0               trust
```
## Create schema plm
```
CREATE SCHEMA plm;
```

## Add the following line to the postgresql.conf
```
listen_addresses = '*'
port = 5432
```

# Kubernetes networking on Mac OS (IP address may change based on your network)
## Add the following line to the /etc/hosts
## replace the minikube_ip using the command minikube ip
```
192.168.64.1    host.minikube.internal
minikube_ip     macbook.local

```

# Start minikube on Mac
## Commands
```
minikube start --driver=hyperkit
eval $(minikube docker-env)
minikube addons enable ingress

```

# Create container image using docker
## Build the docker image without cache
```
docker build --no-cache -t plm-microservices-app:latest .
```

# Deploy K8s file using the commands below
```
 kubectl create namespace plm
 kubectl apply -f configmap.yaml -n plm
 kubectl apply -f secret.yaml -n plm
 kubectl apply -f deployment.yaml -n plm
 kubectl apply -f service.yaml -n plm
 kubectl apply -f clusterissuer.yaml -n plm
 kubectl apply -f certificate.yaml -n plm
 kubectl apply -f ingress.yaml -n plm

```
# Generate the service url using the command below
```
minikube service web-app-service -n plm
```
```
|-----------|-----------------|-------------|---------------------------|
| NAMESPACE |      NAME       | TARGET PORT |            URL            |
|-----------|-----------------|-------------|---------------------------|
| plm       | web-app-service |          80 | http://192.168.64.2:31000 |
|-----------|-----------------|-------------|---------------------------| 
```

# Running the application - REST API using Swagger
```
Hit the url - https://192.168.64.2:31000/docs ( if ingress is not configured )
URL - https://macbook.local/docs ( if ingress is configured, USE THIS)
```
# Use case 1: Create Parts

REST API - /parts/
## Create Axle (Part)
![img.png](img.png)

## Create Wheel (Part)
![img_5.png](img_5.png)


# Use case 2: Create Drawings

## Create Drawing (Connect the Axle and Wheel to the Drawing)
![img_6.png](img_6.png)


# Use case 3: Containerize the app using Docker
Pods running in the minikube
![img_7.png](img_7.png)

# Use case 4: Orchestrate the app using Kubernetes
![img_8.png](img_8.png)


# Use case 5: Deploy the app on Kubernetes
![img_9.png](img_9.png)
