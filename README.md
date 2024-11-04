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
## Check database connection (postgres) from pod
```
nc -vz localhost 5432
```
# Kubernetes networking on Mac OS (IP address may change based on your network)
 Add the following line to the /etc/hosts (host.minikube.internal points to the ip address on your local mac)
 
 This can be obtained from mac by running command ifconfig and then getting the ip for bridge100, this ip is the host.minikube.internal
 
 Replace the minikube_ip using the command minikube ip

 As a side note Docker desktop is not running on mac 
```
192.168.64.1    host.minikube.internal
minikube_ip     macbook.local

```

# Start minikube on Mac
## Commands
```
minikube start --driver=hyperkit
minikube -p minikube docker-env                                                                                      ─╯
eval $(minikube docker-env)
minikube addons enable ingress
```

# Create container image using docker
## Build the docker image without cache
```
docker build --no-cache -t plm-microservices-app:latest .
```
## Run the docker container on Ubuntu with the flag --net=host, so no need to use host.docker.internal on ubuntu only
``` 
docker run --net=host -p 8000:8000 plm-microservices-app:latest

```

# Deploy K8s file using the commands below
```
 kubectl apply -f namespace.yaml
 kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.6.1/cert-manager.yaml
 kubectl apply -f configmap.yaml -n plm
 kubectl apply -f secret.yaml -n plm
 kubectl apply -f deployment.yaml -n plm
 kubectl apply -f service.yaml -n plm
 kubectl apply -f clusterissuer.yaml -n plm
 kubectl apply -f certificate.yaml -n plm
 kubectl apply -f ingress.yaml -n plm
 kubectcl apply -f test-pod.yaml -n plm

```
# Test POD - Debugging (Optional)
```
kubectl exec -it test-pod -n plm -- sh
```
# Generate the service url using the command below

```
minikube service web-app-service -n plm
```
```
|-----------|-----------------|-------------|----------------------------|
| NAMESPACE |      NAME       | TARGET PORT |            URL             |
|-----------|-----------------|-------------|----------------------------|
| plm       | web-app-service |          80 | http://192.168.64.14:31000 |
|-----------|-----------------|-------------|----------------------------|
🎉  Opening service plm/web-app-service in default browser...
```

# Running the application - REST API using Swagger
```
Hit the url - http://192.168.64.14:31000/ ( if ingress is not configured , works on mac with hyperkit)
URL - https://macbook.local/docs ( if ingress is configured, USE THIS, works on mac with hyperkit)
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
