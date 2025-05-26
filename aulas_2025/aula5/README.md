# Laboratório Atualizado: Kubernetes Dashboard e Aplicação httpbin - AWS Academy

Este guia mostra como configurar e utilizar o Kubernetes Dashboard no ambiente AWS Academy, uma interface gráfica para gerenciar seu cluster Kubernetes. Ele abrange:
- Criação de um cluster Kind com mapeamento de portas
- Instalação e acesso ao Kubernetes Dashboard via IP público da EC2
- Configuração de uma conta de serviço com permissões administrativas
- Implantação de uma aplicação httpbin

✅ **Data da Atualização: 21 de Maio de 2025**

---

## 1. Configuração do Ambiente

### 1.1. Baixar os Arquivos de Configuração
```bash
# Baixe os arquivos de configuração (execute na instância EC2 da AWS Academy)
wget https://raw.githubusercontent.com/able2cloud/continuous_monitoring_log_analytics/refs/heads/main/aulas_2025/aula5/kind-config.yaml
wget https://raw.githubusercontent.com/able2cloud/continuous_monitoring_log_analytics/refs/heads/main/aulas_2025/aula5/kubernetes-dashboard-nodeport.yaml
wget https://raw.githubusercontent.com/able2cloud/continuous_monitoring_log_analytics/refs/heads/main/aulas_2025/aula5/dashboard-admin-sa-token.yaml
wget https://raw.githubusercontent.com/able2cloud/continuous_monitoring_log_analytics/refs/heads/main/aulas_2025/aula5/httpbinfull.yaml
```

### 1.2. Criar Cluster Kind
Primeiro, crie um arquivo chamado `kind-config.yaml` com o seguinte conteúdo exato:
```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: aulafive
nodes:
  - role: control-plane
    extraPortMappings:
      - containerPort: 30443
        hostPort: 8443
        protocol: TCP
      - containerPort: 30080
        hostPort: 8080
        protocol: TCP
```

Depois, crie o cluster (certifique-se de estar no diretório onde salvou o arquivo):
```bash
# Criar o Cluster com Kind (execute na instância EC2 da AWS Academy)
sudo kind create cluster --config kind-config.yaml

# Verificar o cluster
sudo kubectl get nodes
```

---

## 2. Instalação do Kubernetes Dashboard

### 2.1. Instalar o Dashboard
```bash
# Instalar o Kubernetes Dashboard (execute na instância EC2 da AWS Academy)
sudo kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# Aguarde os pods subirem (pode levar 1-2 minutos)
sudo kubectl get pods -n kubernetes-dashboard --watch
# Pressione Ctrl+C quando todos os pods estiverem em estado Running

# Criar o serviço NodePort para o Dashboard
sudo kubectl apply -f kubernetes-dashboard-nodeport.yaml

# Verificar se o serviço foi criado corretamente
sudo kubectl get svc -n kubernetes-dashboard
```

---

## 3. Configuração de Acesso ao Dashboard

### 3.1. Criar Conta de Serviço e Permissões
```bash
# Criar uma Conta de Serviço e Cluster Role Binding (execute na instância EC2 da AWS Academy)
sudo kubectl create serviceaccount dashboard-admin-sa -n default
sudo kubectl create clusterrolebinding dashboard-admin-sa --clusterrole=cluster-admin --serviceaccount=default:dashboard-admin-sa

# Verificar se a conta de serviço foi criada
sudo kubectl get serviceaccount dashboard-admin-sa -n default
```

### 3.2. Configurar Token de Acesso
```bash
# Criar o token (execute na instância EC2 da AWS Academy)
sudo kubectl apply -f dashboard-admin-sa-token.yaml

# Aguarde alguns segundos e obtenha o Token de Acesso
sudo kubectl describe secret dashboard-admin-sa-token -n default

# Alternativamente, você pode obter apenas o token:
sudo kubectl get secret dashboard-admin-sa-token -n default -o jsonpath='{.data.token}' | base64 --decode
```

**Importante:** Copie e salve o token obtido, pois você precisará dele para fazer login no Dashboard.

---

## 4. Acessar o Dashboard

### 4.1. Verificar a Configuração do Serviço
```bash
# Verificar se o serviço NodePort está configurado corretamente
sudo kubectl get svc kubernetes-dashboard-nodeport -n kubernetes-dashboard

# Deve mostrar algo como:
# NAME                            TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE
# kubernetes-dashboard-nodeport   NodePort   10.96.xxx.xxx   <none>        443:30443/TCP   xxm
```

### 4.2. Acessar via IP Público da EC2
**No ambiente AWS Academy, acesse via navegador:**
```
https://<IP_PUBLICO_DA_EC2>:8443
```

**Onde:**
- `<IP_PUBLICO_DA_EC2>` deve ser substituído pelo endereço IP público da sua instância EC2 da AWS Academy
- A porta `8443` está mapeada para a porta `30443` do serviço NodePort do Dashboard
- **Importante:** Use `https://` (não `http://`)

**Para encontrar o IP público da sua instância EC2:**
1. Acesse o console da AWS Academy
2. Vá para EC2 > Instances
3. Localize sua instância e copie o "Public IPv4 address"

### 4.3. Passos para Acessar pelo Navegador
1. Abra seu navegador e acesse a URL: `https://<IP_PUBLICO_DA_EC2>:8443/`
2. **Aceite o certificado não confiável** (clique em "Advanced" > "Proceed to [IP] (unsafe)" no Chrome/Edge, ou equivalente no Firefox)
3. Quando a página de login do Kubernetes Dashboard aparecer, selecione a opção **Token**
4. Cole o token obtido anteriormente no campo de token
5. Clique em **Sign In**

**Observação:** É normal que o navegador exiba um aviso de certificado não confiável, pois estamos usando um certificado auto-assinado. Isso é seguro em um ambiente de laboratório.

---

## 5. Implantação da Aplicação httpbin

### 5.1. Criar o Deployment e Serviço
```bash
# Criar o httpbin (execute na instância EC2 da AWS Academy)
sudo kubectl apply -f httpbinfull.yaml

# Verificar se a aplicação foi implantada
sudo kubectl get deployments
sudo kubectl get pods
sudo kubectl get services

# Aguarde os pods ficarem em estado Running
sudo kubectl get pods --watch
# Pressione Ctrl+C quando os pods estiverem em Running
```

### 5.2. Verificar e Acessar o httpbin
```bash
# Verificar a porta do serviço httpbin
sudo kubectl get svc httpbin-service -o jsonpath='{.spec.ports[0].nodePort}'

# O comando acima deve retornar 30080
```

**Acesse o httpbin via navegador:**
```
http://<IP_PUBLICO_DA_EC2>:8080
```

**Onde:**
- `<IP_PUBLICO_DA_EC2>` é o mesmo IP público da sua instância EC2
- A porta `8080` está mapeada para a porta `30080` do serviço NodePort do httpbin
- **Importante:** Use `http://` (não `https://`) para o httpbin

### 5.3. Alternativa: Converter Serviço ClusterIP para NodePort (Útil com Helm)
Se você tiver um serviço que foi criado como ClusterIP (comum com instalações Helm) e precisar expô-lo, use o `kubectl patch`:

```bash
# Exemplo: Se o httpbin fosse criado como ClusterIP, você poderia convertê-lo assim:
sudo kubectl patch svc httpbin-service \
  -p '{
    "spec": {
      "type": "NodePort",
      "ports": [
        {
          "name": "http",
          "port": 80,
          "targetPort": 80,
          "nodePort": 30080,
          "protocol": "TCP"
        }
      ]
    }
  }'

# Verificar a mudança
sudo kubectl get svc httpbin-service
```

**Quando usar este comando:**
- Quando você instala aplicações via Helm que não oferecem opção de NodePort
- Quando você precisa expor um serviço ClusterIP existente
- Para modificar a porta NodePort de um serviço existente

### 5.4. Verificar no Dashboard
Navegue até os recursos do Kubernetes Dashboard para visualizar o httpbin que foi criado, verificando:

1. **Workloads** → **Deployments**: Você deve ver o deployment `httpbin`
2. **Workloads** → **Pods**: Você deve ver os pods do httpbin em execução
3. **Service and Discovery** → **Services**: Você deve ver o serviço `httpbin-service`
4. **Config and Storage**: Explore outras configurações se necessário

### 5.5. Testar o httpbin
```bash
# Teste local para verificar se o httpbin está respondendo
curl http://localhost:8080

# Teste uma rota específica do httpbin
curl http://localhost:8080/get

# Verificar logs dos pods httpbin (opcional)
sudo kubectl logs -l app=httpbin
```

---

## 6. Explorando o Kubernetes Dashboard

### 6.1. Recursos Importantes para Verificar
No Dashboard, explore as seguintes seções:

1. **Overview**: Visão geral do cluster
2. **Workloads**:
   - **Deployments**: Todos os deployments (httpbin, dashboard, etc.)
   - **Pods**: Todos os pods em execução
   - **Replica Sets**: Conjuntos de réplicas
3. **Service and Discovery**:
   - **Services**: Todos os serviços (httpbin-service, dashboard, etc.)
   - **Ingresses**: Regras de ingress (se houver)
4. **Config and Storage**:
   - **Config Maps**: Configurações
   - **Secrets**: Informações sensíveis (tokens, senhas)
5. **Cluster**:
   - **Nodes**: Informações dos nós do cluster
   - **Namespaces**: Todos os namespaces

### 6.2. Monitoramento em Tempo Real
- Use a funcionalidade de **logs** para ver logs dos pods em tempo real
- Monitore o uso de **CPU e memória** dos pods
- Verifique **eventos** para troubleshooting

---

## 7. Verificação e Troubleshooting

### 7.1. Verificações Básicas
```bash
# Verificar se todos os pods estão rodando
sudo kubectl get pods -A

# Verificar serviços
sudo kubectl get svc -A

# Verificar se o cluster está saudável
sudo kubectl cluster-info

# Verificar eventos recentes
sudo kubectl get events --sort-by=.metadata.creationTimestamp
```

### 7.2. Problemas Comuns

**Dashboard não carrega:**
```bash
# Verificar se os pods do dashboard estão rodando
sudo kubectl get pods -n kubernetes-dashboard

# Verificar logs do dashboard
sudo kubectl logs -n kubernetes-dashboard -l k8s-app=kubernetes-dashboard
```

**Token não funciona:**
```bash
# Verificar se o secret existe
sudo kubectl get secret dashboard-admin-sa-token -n default

# Obter um novo token
sudo kubectl get secret dashboard-admin-sa-token -n default -o jsonpath='{.data.token}' | base64 --decode
```

**httpbin não acessível:**
```bash
# Verificar se o pod está rodando
sudo kubectl get pods -l app=httpbin

# Verificar o serviço
sudo kubectl get svc httpbin-service

# Testar localmente primeiro
curl http://localhost:8080
```

---

## 8. Limpeza dos Recursos
```bash
# Para limpar os recursos (execute na instância EC2 da AWS Academy):
sudo kubectl delete -f httpbinfull.yaml
sudo kubectl delete -f dashboard-admin-sa-token.yaml
sudo kubectl delete clusterrolebinding dashboard-admin-sa
sudo kubectl delete serviceaccount dashboard-admin-sa -n default
sudo kubectl delete -f kubernetes-dashboard-nodeport.yaml
sudo kubectl delete -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# Para remover completamente o cluster Kind:
sudo kind delete cluster --name aulafive
```

---

## 9. Considerações para AWS Academy

### 9.1. Security Groups
Certifique-se de que o Security Group da instância EC2 permite:
- **Porta 8443** (HTTPS) para o Kubernetes Dashboard
- **Porta 8080** (HTTP) para o httpbin

### 9.2. Certificados SSL
- O Dashboard usa certificados auto-assinados, então o navegador mostrará avisos de segurança
- Isso é normal e seguro em um ambiente de laboratório
- Sempre use `https://` para o Dashboard e `http://` para o httpbin

### 9.3. Limpeza
- Sempre limpe os recursos ao final do laboratório para evitar custos desnecessários
- Execute `sudo kind delete cluster --name aulafive` para remover tudo

---

Com isso, você tem um Kubernetes Dashboard funcionando no AWS Academy, acessível via IP público da EC2, com uma aplicação httpbin para demonstração e uma interface gráfica completa para gerenciar seu cluster Kubernetes. 