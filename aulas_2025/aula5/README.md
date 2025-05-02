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
kind create cluster --name aula5

# Verificar o cluster
kubectl get nodes
```

---

## 2. Instalação do Kubernetes Dashboard

### 2.1. Instalar o Dashboard
```bash
# Instalar o Kubernetes Dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```

### 2.2. Configurar o Node para o Ingress
```bash
kubectl label node ingress-lab-control-plane ingress-ready=true
kubectl label node ingress-lab-control-plane kubernetes.io/os=linux
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
# Baixar o arquivo dashboard-admin-sa-token.yaml
wget https://raw.githubusercontent.com/able2cloud/continuous_monitoring_log_analytics/main/aulas_2024/aula5/dashboard-admin-sa-token.yaml

# Criar o token
kubectl apply -f dashboard-admin-sa-token.yaml

# Obter o Token de Acesso
kubectl describe secret dashboard-admin-sa-token -n default
```

---

## 4. Acessar o Dashboard

### 4.1. Configurar Port-Forward
```bash
# Fazer o Port-Forward para Acessar o Dashboard
kubectl port-forward svc/kubernetes-dashboard -n kubernetes-dashboard 8001:443
```

### 4.2. Passos para Acessar pelo Navegador
1. Abra seu navegador e acesse a URL: https://localhost:8001/
2. Quando a página de login do Kubernetes Dashboard aparecer, selecione a opção Token e cole o token obtido anteriormente.
3. Clique em Sign In.

---

## 5. Implantação da Aplicação httpbin

### 5.1. Criar o Deployment e Serviço
```bash
# Criar o httpbin
kubectl apply -f https://raw.githubusercontent.com/able2cloud/continuous_monitoring_log_analytics/main/aulas_2024/aula5/httpbinfull.yaml
```

### 5.2. Verificar no Dashboard
Navegue até os recursos do Kubernetes Dashboard para visualizar o httpbin que foi criado, verificando:
- Deployments
- Pods
- Services
- Outros recursos associados 