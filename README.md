A Python FastAPi application with Postgres databse, Docker containerization, Kubernetes Orchestration, Github Actions CI, ArgoCD for CD and Nginx GatewayAPI
for routing and external access.

# Running Locally

## Clone this repository
```
git clone https://github.com/Sp3aR007/FastAPI.git
```

## Build Docker image

```
docker build -t sp3ar007/fastapi .
```
## Using Docker compose for dev environment
```
docker-compose -f docker-compose-dev.yaml up -d
```
## Using Dokcer compose for production environment
```
docker-compose -f docker-compose-prod.yaml up -d
```

# Kubernetes Deployment Details 

## Install CLoudnativePG 
```
kubectl apply --server-side -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.23/releases/cnpg-1.23.1.yaml
```

## Apply secrets required for the Postgres database
```
kubectl apply -f deploy/secret.yaml
```

## Deploy Postgres cluster 
```
kubectl apply -f deploy/postgres-cluster.yaml
```

## Exec into postgres instance and intialize the database in the cluster
```
kubectl exec -it my-postgresql-1 -- psql -U postgres -c "ALTER USER fastapi WITH PASSWORD 'fastapi';" 
```

## Creating table inside the database
```
kubectl port-forward my-postgresql-1 5432:5432
PGPASSWORD='fastapi' psql -h 127.0.0.1 -U fastapi -d fastapi -c "

CREATE TABLE fastapi ();
"
```

## Create the deployment 
```
kubectl create -f deploy/deploy.yaml
```

## Install Certmanager
```
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.15.3/cert-manager.yaml
```

## Edit the cert-manager deployment and add enable-gatweay-api in args section of cert-manager deployment
``` 
kubectl edit deploy/cert-manager -n cert-manager
```
``` 
- --enable-gateway-api 
```

## Restart the deployment to apply the changes done to cert-manager deployment configuration
```
kubectl rollout restart deployment cert-manager -n cert-manager
```

## Appy the service configuration
```
kubectl apply -f deploy/service.yaml
```

## Install the Nginx gateway fabric
```
kubectl kustomize "https://github.com/nginxinc/nginx-gateway-fabric/config/crd/gateway-api/standard?ref=v1.3.0" | kubectl apply -f - 
```
```
helm install ngf oci://ghcr.io/nginxinc/charts/nginx-gateway-fabric --create-namespace -n nginx-gateway
```

## Create the gateway class and route
```
kubectl create -f deploy/gateway.yaml 
```
``` 
kubectl create -f deploy/app-route.yaml
```

## Create CLuster issuer for the SSL Certificate
```  
kubectl create -f deploy/cluster_issuer.yaml
```


## ArgoCD Installation
```
kubectl create namespace argocd
```
```
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
```
kubectl patch configmap argocd-cmd-params-cm  -n argocd --patch '{"data":{"server.insecure":"true"}}'
```
```
kubectl rollout restart deployment argocd-server -n argocd 
```

## Get ArgoCD Password to login to the argo server
``` 
kubectl get secret --namespace argocd argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode ; echo 
```

# Deployment details

## AWS 

### Normal deployment

[!aws-deploy](images/aws-normal-deploy.png)

[!aws-deploy-1](images/aws-normal-deploy-1.png)

### Nginx webserver

[!aws-nginx](images/aws-with-nginx.png)

[!aws-nginx-ec2-dns](images/aws-with-nginx-ec2dns.png)

### SSL encryption

[!aws-nginx-ssl](images/aws-nginx-with-ssl.png)

### AWS CI/CD

[!aws-ci/cd](images/proper-deploy-with-cicd.png)


## Kubernetes 

### Kubernetes deployment

[!k8s-deploy](images/k8s-deploy.png)

### Continuous Deployment with ArgoCD

[!k8s-argocd](images/k8s-argocd.png)

### CI/CD with Github Actions and ArgoCD

[!k8s-ci/cd](images/k8s-cicd-with-argocd.png)

