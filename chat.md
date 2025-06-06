Perfect — here's your **0 → 1 setup** to build a single Git repo for deploying multiple scripts via **Argo CD**, using **Minikube** locally for testing.

---

## ✅ Goal

* One Git repo (`infra-scripts/`)
* Each script in its own folder (`/script1`, `/script2`, ...)
* Argo CD auto-deploys each via an **ApplicationSet**
* No secrets for now

---

## 🔧 Step-by-Step

```sh
minikube delete && \
minikube start --driver=docker && \
eval $(minikube docker-env) && \
kubectl create namespace argocd && \
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml && \
docker build -t script1:latest ./script1 && \
docker build -t script2:latest ./script2 && \
kubectl wait pod -l app.kubernetes.io/name=argocd-application-controller -n argocd --for=condition=Ready --timeout=180s && \
kubectl wait deployment argocd-server -n argocd --for=condition=Available --timeout=180s && \
kubectl apply -f applicationset.yaml -n argocd && \
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d && \
echo && \
open http://localhost:8080 && \
kubectl port-forward svc/argocd-server -n argocd 8080:443 > /dev/null 2>&1 &
```

to set up sealed secrets:
```sh
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/latest/download/controller.yaml
kubeseal --fetch-cert > sealed-secrets.crt
```

to create a sealed secret:
```sh
# uncomment dummy-secret.yaml
# value must be base64 encoded, so

# echo 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80 | base64

kubeseal --cert sealed-secrets.crt -o yaml < dummy-secret.yaml > ./long-script/real-sealed-secret.yaml

```

### 1. **Start Minikube**

```sh
minikube start --driver=docker
eval $(minikube docker-env)
```

---

### 2. **Install Argo CD**

```sh
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

---

### 3. **Create Your Repo Structure**

```bash
infra-scripts/
├── script1/
│   ├── Dockerfile
│   ├── script.py
│   └── deployment.yaml
├── script2/
│   └── ...
└── applicationset.yaml
```

---

### 4. **Example `Dockerfile` for a script**

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY script.py .
CMD ["python", "script.py"]
```

---

### 5. **Example `deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: script1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: script1
  template:
    metadata:
      labels:
        app: script1
    spec:
      containers:
      - name: script1
        image: script1:latest
        imagePullPolicy: Never
```

---

### 6. **Build Images in Minikube Docker**

```sh
docker build -t script1:latest ./script1
docker build -t script2:latest ./script2
```

---

### 7. **Create `applicationset.yaml`**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: infra-scripts
  namespace: argocd
spec:
  generators:
    - git:
        repoURL: https://github.com/your-username/infra-scripts
        revision: main
        directories:
          - path: '*'
  template:
    metadata:
      name: '{{path.basename}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/your-username/infra-scripts
        targetRevision: main
        path: '{{path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: default
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

---

### 8. **Apply ApplicationSet**

```sh
kubectl apply -f applicationset.yaml -n argocd
```

---

### 9. **Push to GitHub**

Push the `infra-scripts` repo to GitHub.

---

### 10. **Verify in Argo UI**

Go to [https://localhost:8080](https://localhost:8080)
Login with:

```sh
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

---

## ✅ You're Done

Now every new folder (e.g., `script3/`) you add and push will be:

* Auto-detected by Argo CD
* Auto-deployed as a new Kubernetes Application

Let me know if you want a repo template zipped or hosted.
