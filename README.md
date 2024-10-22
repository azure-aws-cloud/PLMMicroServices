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

## Add the following line to the postgresql.conf
```
listen_addresses = '*'
port = 5432
```

# Kubernetes networking on Mac OS (IP address may change based on your network)
## Add the following line to the /etc/hosts
```
192.168.64.1    host.minikube.internal
```

# Use case 1: Create Parts

# Use case 2: Create Drawings

# Use case 3: Containerize the app using Docker

# Use case 4: Orchestrate the app using Kubernetes

# Use case 5: Deploy the app on Kubernetes

