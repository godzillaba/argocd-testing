# argocd-testing

```sh
minikube delete && \
minikube start --driver=docker && \
eval $(minikube docker-env) && \
kubectl create namespace argocd && \
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml && \
docker build -t propmon:latest -f ./dockerfiles/Dockerfile.propmon . && \
docker build -t cast-send:latest -f ./dockerfiles/Dockerfile.cast-send . && \
docker build -t fund-distribution-scripts:latest -f ./dockerfiles/Dockerfile.fund-distribution-scripts . && \
docker build -t block-hash-pusher:latest -f ./dockerfiles/Dockerfile.block-hash-pusher . && \
kubectl wait pod -l app.kubernetes.io/name=argocd-application-controller -n argocd --for=condition=Ready --timeout=180s && \
kubectl wait deployment argocd-server -n argocd --for=condition=Available --timeout=180s && \
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/latest/download/controller.yaml && \
kubectl wait --for=condition=available deployment sealed-secrets-controller -n kube-system --timeout=60s && \
kubeseal --fetch-cert > sealed-secrets.crt && \
kubeseal --cert sealed-secrets.crt -o yaml < real-secrets/propmon-secret.yaml > ./raw/secrets/propmon-sealed-secret.yaml && \
kubeseal --cert sealed-secrets.crt -o yaml < real-secrets/fund-distribution-secret.yaml > ./raw/secrets/fund-distribution-sealed-secret.yaml && \
kubeseal --cert sealed-secrets.crt -o yaml < real-secrets/flush-timeboost-secret.yaml > ./raw/secrets/flush-timeboost-sealed-secret.yaml && \
kubectl apply -f applicationset.yaml -n argocd && \
kubectl apply -f fund-distribution-applicationset.yaml -n argocd && \
kubectl apply -f bhp-applicationset.yaml -n argocd && \
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d && \
echo && \
open http://localhost:8080 && \
kubectl port-forward svc/argocd-server -n argocd 8080:443 > /dev/null 2>&1 &
```