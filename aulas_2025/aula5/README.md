# Laboratório Atualizado: Kubernetes Dashboard e Aplicação httpbin

Este guia mostra como configurar e utilizar o Kubernetes Dashboard, uma interface gráfica para gerenciar seu cluster Kubernetes. Ele abrange:
- Criação de um cluster Kind
- Instalação e acesso ao Kubernetes Dashboard
- Configuração de uma conta de serviço com permissões administrativas
- Implantação de uma aplicação httpbin

✅ **Data da Atualização: 7 de Abril de 2025**

---

## 1. Configuração do Ambiente

### 1.1. Criar Cluster Kind
```bash
# Criar o Cluster com Kind
kind create cluster --config kind-config.yaml

# Verificar o cluster
kubectl get nodes
```

---

## 2. Instalação do Kubernetes Dashboard

### 2.1. Instalar o Dashboard
```bash
# Instalar o Kubernetes Dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# Criar o serviço NodePort para o Dashboard
kubectl apply -f kubernetes-dashboard-nodeport.yaml
```

---

## 3. Configuração de Acesso ao Dashboard

### 3.1. Criar Conta de Serviço e Permissões
```bash
# Criar uma Conta de Serviço e Cluster Role Binding
kubectl create serviceaccount dashboard-admin-sa -n default
kubectl create clusterrolebinding dashboard-admin-sa --clusterrole=cluster-admin --serviceaccount=default:dashboard-admin-sa
```

### 3.2. Configurar Token de Acesso
```bash
# Criar o token
kubectl apply -f dashboard-admin-sa-token.yaml

# Obter o Token de Acesso
kubectl describe secret dashboard-admin-sa-token -n default
```

---

## 4. Acessar o Dashboard

### 4.1. Obter a Porta do Dashboard
```bash
# Obter a porta do serviço Dashboard
kubectl get svc kubernetes-dashboard-nodeport -n kubernetes-dashboard -o jsonpath='{.spec.ports[0].nodePort}'
# Use o número da porta retornado acima para acessar o Dashboard
# Exemplo: https://<IP_PUBLICO_DA_EC2>:<PORTA>
```

### 4.2. Passos para Acessar pelo Navegador
1. Abra seu navegador e acesse a URL: https://<IP_PUBLICO_DA_EC2>:<PORTA>/
2. Quando a página de login do Kubernetes Dashboard aparecer, selecione a opção Token e cole o token obtido anteriormente.
3. Clique em Sign In.

---

## 5. Implantação da Aplicação httpbin

### 5.1. Criar o Deployment e Serviço
```bash
# Criar o httpbin
kubectl apply -f httpbinfull.yaml

# Verificar a porta do serviço httpbin
kubectl get svc httpbin-service -o jsonpath='{.spec.ports[0].nodePort}'
# Use o número da porta retornado acima para acessar o httpbin
# Exemplo: http://<IP_PUBLICO_DA_EC2>:<PORTA>
```

### 5.2. Verificar no Dashboard
Navegue até os recursos do Kubernetes Dashboard para visualizar o httpbin que foi criado, verificando:
- Deployments
- Pods
- Services
- Outros recursos associados 

---

## 6. Limpeza dos Recursos
```bash
# Para limpar os recursos:
kubectl delete -f httpbinfull.yaml
kubectl delete -f kubernetes-dashboard-nodeport.yaml
kubectl delete -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
kubectl delete -f dashboard-admin-sa-token.yaml

kind delete cluster --name aulafive
``` 