# Laboratório Atualizado: Configuração de Ingress NGINX no Kubernetes

Este guia demonstra como configurar e utilizar o Ingress NGINX no Kubernetes. Ele abrange:
- Criação de um cluster Kind otimizado para Ingress
- Instalação e configuração do Ingress NGINX Controller
- Implantação de uma aplicação de exemplo
- Criação e teste de regras de Ingress

✅ **Data da Atualização: 7 de Abril de 2025**

---

## 1. Configuração do Ambiente

### 1.1. Criar Cluster Kind
```bash
# Criar um cluster Kind
kind create cluster --config kind-config.yaml

# Verificar o cluster
kubectl get nodes
```

---

## 2. Instalação do Ingress NGINX Controller

### 2.1. Instalar o NGINX Ingress Controller
```bash
# Adicionar o repositório do Ingress NGINX
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# Verificar a instalação
kubectl get pods -n ingress-nginx --watch
```

---

## 3. Implantação da Aplicação de Exemplo

### 3.1. Criar um Deployment e um Serviço
```bash
# Criar um deployment e um serviço
kubectl create deployment hello-world --image=gcr.io/google-samples/hello-app:1.0
kubectl expose deployment hello-world --port=8080 --target-port=8080

# Verificar os serviços
kubectl get svc
```

---

## 4. Configuração do Ingress

### 4.1. Criar um Arquivo YAML para o Ingress
```bash
cat <<EOF > ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: hello-world-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: hello-world.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: hello-world
            port:
              number: 8080
EOF
```

### 4.2. Aplicar o Ingress Resource
```bash
# Aplicar o Ingress Resource
kubectl apply -f ingress.yaml
```

---

## 5. Configuração e Teste do Acesso

### 5.1. Configurar Resolução de Nome Local
```bash
# Adicionar uma entrada no arquivo hosts para apontar hello-world.local para o endereço IP do cluster Kind
sed -i '$ a\127.0.0.1 hello-world.local' /etc/hosts
```

### 5.2. Testar o Acesso via Ingress
```bash
# Testar o acesso via Ingress usando curl
curl http://hello-world.local
```

---

## 6. Verificação e Diagnóstico

### 6.1. Verificar os Logs do Ingress Controller
```bash
# Verificar os logs do Ingress Controller
kubectl logs -n ingress-nginx --tail 10 -l app.kubernetes.io/name=ingress-nginx

# Verificar os eventos
kubectl get events --namespace ingress-nginx
```

---

## 7. Limpeza dos Recursos
```bash
# Para limpar os recursos:
kubectl delete -f ingress.yaml
kubectl delete service hello-world
kubectl delete deployment hello-world
kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

kind delete cluster --name ingress-lab
``` 