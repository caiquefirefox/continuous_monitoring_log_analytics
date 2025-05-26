# Laboratório Atualizado: Kubernetes Local com Kind (e Pré-requisitos Docker) - AWS Academy

Este guia mostra como configurar um ambiente Kubernetes local usando **Kind** no ambiente AWS Academy. Ele cobre:
- Instalação dos pré-requisitos essenciais: Docker e Docker Compose
- Instalação do Kind, Kubectl e Helm
- Implantação de uma aplicação Nginx simples em um namespace
- Configuração para acesso via IP público da instância EC2

✅ **Data da Atualização: 21 de Maio de 2025**

---

## 1. Instalação dos Pré-requisitos Essenciais

### 1.1. Docker e Docker Compose (Linux/AWS Academy)

**Para ambiente AWS Academy (Ubuntu/Amazon Linux):**

Remova versões antigas (se houver):
```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

Atualize pacotes e instale pré-requisitos:
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
```

Adicione a chave e repositório oficial:
```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

Instale o Docker Engine e Compose Plugin:
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Pós-instalação:
```bash
sudo usermod -aG docker $USER
# Para aplicar as mudanças sem reiniciar:
newgrp docker
```

Verificação:
```bash
docker --version
docker compose version
sudo systemctl status docker
sudo docker run hello-world
```

Referência oficial: https://docs.docker.com/engine/install/ubuntu/

---

## 2. Instalação das Ferramentas Kubernetes

### 2.1. Kind (Kubernetes in Docker)

**Linux (AWS Academy)**:
```bash
# Execute na instância EC2 da AWS Academy
curl -Lo ./kind "https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64"
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

Verifique:
```bash
sudo kind --version
```

### 2.2. Kubectl

**Linux (AWS Academy)**:
```bash
# Execute na instância EC2 da AWS Academy
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
```

Verificação:
```bash
sudo kubectl version --client
```

### 2.3. Helm (Gerenciador de Pacotes Kubernetes)

**Linux (via script oficial)**:
```bash
# Execute na instância EC2 da AWS Academy
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
sudo ./get_helm.sh
```

Verificação:
```bash
sudo helm version
```

---

## 3. Criação e Interação com o Cluster Kind

### 3.1. Baixar os Arquivos de Configuração
```bash
# Baixe os arquivos de configuração (execute na instância EC2 da AWS Academy)
wget https://raw.githubusercontent.com/able2cloud/continuous_monitoring_log_analytics/refs/heads/main/aulas_2025/aula1/kind-config.yaml
wget https://raw.githubusercontent.com/able2cloud/continuous_monitoring_log_analytics/refs/heads/main/aulas_2025/aula1/nginx-app.yaml
```

### 3.2. Criar o Cluster
Primeiro, crie um arquivo chamado `kind-config.yaml` com o seguinte conteúdo exato:
```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: aulaone
nodes:
  - role: control-plane
    extraPortMappings:
      - containerPort: 30080
        hostPort: 8080
        protocol: TCP
```

Depois, crie o cluster (certifique-se de estar no diretório onde salvou o arquivo):
```bash
# Crie um cluster no KIND (execute na instância EC2 da AWS Academy)
sudo kind create cluster --config kind-config.yaml

# Verifique se o cluster foi criado corretamente
sudo kubectl get nodes
```

### 3.3. Verificar o Cluster
```bash
# Verifique se o cluster está acessível
sudo kubectl cluster-info --context kind-aulaone
sudo kubectl get nodes

# Liste os clusters Kind disponíveis
sudo kind get clusters
```

### 3.4. Criar um Namespace
```bash
sudo kubectl create namespace aula1
sudo kubectl get namespaces
```

---

## 4. Implantar uma Aplicação Nginx de Exemplo

### 4.1. Aplicar o Manifesto
```bash
# Aplicar o manifesto do Nginx (execute na instância EC2 da AWS Academy)
sudo kubectl apply -f nginx-app.yaml

# Verifique se a aplicação foi implantada corretamente
sudo kubectl get deployment -n aula1
sudo kubectl get pods -n aula1 -o wide
sudo kubectl get service -n aula1
```

### 4.2. Verificar a Aplicação
```bash
# Verificar o deployment
sudo kubectl get deployment -n aula1
# Deve mostrar nginx-deployment com 2/2 replicas prontas

# Verificar os pods
sudo kubectl get pods -n aula1 -o wide
# Deve mostrar 2 pods nginx em estado Running

# Verificar o serviço e obter a porta
sudo kubectl get service -n aula1
# Deve mostrar nginx-service do tipo NodePort na porta 30080
```

### 4.3. Acessar o Nginx

**No ambiente AWS Academy, acesse via navegador:**
```
http://<IP_PUBLICO_DA_EC2>:8080
```

**Onde:**
- `<IP_PUBLICO_DA_EC2>` deve ser substituído pelo endereço IP público da sua instância EC2 da AWS Academy
- A porta `8080` está mapeada para a porta `30080` do serviço NodePort do Nginx

**Para encontrar o IP público da sua instância EC2:**
1. Acesse o console da AWS Academy
2. Vá para EC2 > Instances
3. Localize sua instância e copie o "Public IPv4 address"

### 4.4. Verificar Funcionamento
```bash
# Teste local para verificar se o serviço está respondendo
curl http://localhost:8080

# Verificar logs dos pods (opcional)
sudo kubectl logs -n aula1 -l app=nginx

# Verificar eventos do namespace (para troubleshooting)
sudo kubectl get events -n aula1
```

---

## 5. Limpeza dos Recursos
```bash
# Para limpar os recursos criados:
sudo kubectl delete -f nginx-app.yaml
sudo kubectl delete namespace aula1

# Para remover completamente o cluster Kind:
sudo kind delete cluster --name aulaone
```

---

## 6. Solução de Problemas

### 6.1. Verificações Básicas
```bash
# Verificar se o Docker está rodando
sudo systemctl status docker

# Verificar se o cluster Kind está ativo
sudo kubectl cluster-info

# Verificar todos os pods do sistema
sudo kubectl get pods -A

# Verificar se as portas estão sendo mapeadas corretamente
sudo docker ps | grep aulaone
```

### 6.2. Problemas Comuns

**Erro de permissão com Docker:**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

**Cluster não responde:**
```bash
# Recriar o cluster
sudo kind delete cluster --name aulaone
sudo kind create cluster --config kind-config.yaml
```

**Nginx não acessível:**
- Verifique se o security group da instância EC2 permite tráfego na porta 8080
- Confirme que o IP público está correto
- Teste localmente primeiro: `curl http://localhost:8080`

---

Com isso, você tem um ambiente Kubernetes local funcional no AWS Academy, com Docker, Kind, Kubectl e Helm configurados, e uma aplicação Nginx rodando no namespace `aula1` e acessível via IP público da EC2.

Referências oficiais estão linkadas ao longo do guia para aprofundamento.
