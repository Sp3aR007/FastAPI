## Install CLoudnativePG Database
```
kubectl apply --server-side -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.23/releases/cnpg-1.23.1.yaml
```

## Apply secrets required for the Postgres database
```
kubectl apply -f secret.yaml
```

## Deploy Postgres cluster 
```
kubectl apply -f postgres-cluster.yaml
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
kubectl create -f deploy.yaml
```

## Install Certmanager
```
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.15.3/cert-manager.yaml
```

## Edit the cert-manager deployment and add enable-gatweay-api in args section of cert-manager deployment
``` 
kubectl edit deploy/cert-manager -n cert-manager' 
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
kubectl apply -f service.yaml
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
kubectl create -f gateway.yaml 
```
``` 
kubectl create -f app-route.yaml
```

## Install CLuster issuer for the SSL Certificate
```  
kubectl create -f cluster_issuer.yaml
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