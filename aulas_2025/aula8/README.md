# Laboratório Atualizado: Configuração de Ingress NGINX no Kubernetes - AWS Academy

Este guia demonstra como configurar e utilizar o Ingress NGINX no Kubernetes no ambiente AWS Academy. Ele abrange:
- Criação de um cluster Kind otimizado para Ingress com mapeamento de portas
- Instalação e configuração do Ingress NGINX Controller
- Implantação de uma aplicação de exemplo
- Criação e teste de regras de Ingress via IP público da EC2

✅ **Data da Atualização: 21 de Maio de 2025**

---

## 1. Configuração do Ambiente

### 1.1. Baixar os Arquivos de Configuração
```bash
# Baixe os arquivos de configuração (execute na instância EC2 da AWS Academy)
wget https://raw.githubusercontent.com/able2cloud/continuous_monitoring_log_analytics/refs/heads/main/aulas_2025/aula8/kind-config.yaml
wget https://raw.githubusercontent.com/able2cloud/continuous_monitoring_log_analytics/refs/heads/main/aulas_2025/aula8/hello-world-nodeport.yaml
```

### 1.2. Criar Cluster Kind
Primeiro, crie um arquivo chamado `kind-config.yaml` com o seguinte conteúdo exato:
```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: ingress-lab
nodes:
  - role: control-plane
    kubeadmConfigPatches:
    - |
      kind: InitConfiguration
      nodeRegistration:
        kubeletExtraArgs:
          node-labels: "ingress-ready=true"
    extraPortMappings:
    - containerPort: 80
      hostPort: 8080
      protocol: TCP
    - containerPort: 443
      hostPort: 8443
      protocol: TCP
    - containerPort: 30080
      hostPort: 30080
      protocol: TCP
```

Depois, crie o cluster (certifique-se de estar no diretório onde salvou o arquivo):
```bash
# Criar um cluster Kind (execute na instância EC2 da AWS Academy)
sudo kind create cluster --config kind-config.yaml

# Verificar o cluster
sudo kubectl get nodes
```

---

## 2. Instalação do Ingress NGINX Controller

### 2.1. Instalar o NGINX Ingress Controller
```bash
# Adicionar o repositório do Ingress NGINX (execute na instância EC2 da AWS Academy)
sudo kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# Verificar a instalação
sudo kubectl get pods -n ingress-nginx --watch
# Pressione Ctrl+C quando todos os pods estiverem em estado Running

# Aguarde até que o Ingress Controller esteja pronto (pode levar 2-3 minutos)
sudo kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=300s
```

### 2.2. Verificar a Instalação
```bash
# Verificar se o Ingress Controller está rodando
sudo kubectl get pods -n ingress-nginx

# Verificar os serviços do Ingress NGINX
sudo kubectl get svc -n ingress-nginx

# Deve mostrar o serviço ingress-nginx-controller
```

---

## 3. Implantação da Aplicação de Exemplo

### 3.1. Criar um Deployment e um Serviço
```bash
# Criar um deployment (execute na instância EC2 da AWS Academy)
sudo kubectl create deployment hello-world --image=gcr.io/google-samples/hello-app:1.0

# Expor o deployment como serviço ClusterIP
sudo kubectl expose deployment hello-world --port=8080 --target-port=8080

# Verificar se o deployment foi criado
sudo kubectl get deployments
sudo kubectl get pods
sudo kubectl get services

# Aguarde o pod ficar em estado Running
sudo kubectl get pods --watch
# Pressione Ctrl+C quando o pod estiver Running
```

### 3.2. Criar Serviço NodePort (Para Acesso Direto)
```bash
# Aplicar o serviço NodePort para acesso direto (execute na instância EC2 da AWS Academy)
sudo kubectl apply -f hello-world-nodeport.yaml

# Verificar os serviços
sudo kubectl get svc
# Deve mostrar tanto o serviço ClusterIP quanto o NodePort
```

---

## 4. Configuração do Ingress

### 4.1. Criar um Arquivo YAML para o Ingress
```bash
# Criar o arquivo de configuração do Ingress (execute na instância EC2 da AWS Academy)
cat <<EOF > ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: hello-world-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
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
# Aplicar o Ingress Resource (execute na instância EC2 da AWS Academy)
sudo kubectl apply -f ingress.yaml

# Verificar se o Ingress foi criado
sudo kubectl get ingress

# Verificar detalhes do Ingress
sudo kubectl describe ingress hello-world-ingress
```

---

## 5. Configuração e Teste do Acesso

### 5.1. Testar Acesso Direto via NodePort
```bash
# Verificar a porta NodePort atribuída
sudo kubectl get svc hello-world-nodeport -o jsonpath='{.spec.ports[0].nodePort}'
# Deve retornar 30080
```

**Acesse a aplicação diretamente via navegador:**
```
http://<IP_PUBLICO_DA_EC2>:30080
```

**Onde:**
- `<IP_PUBLICO_DA_EC2>` deve ser substituído pelo endereço IP público da sua instância EC2 da AWS Academy
- A porta `30080` é a porta NodePort configurada

### 5.2. Configurar Acesso via Ingress

#### 5.2.1. Método 1: Usando curl com header Host
```bash
# Testar o Ingress usando curl com header Host (execute na instância EC2 da AWS Academy)
curl -H "Host: hello-world.local" http://localhost

# Ou testando via IP público
curl -H "Host: hello-world.local" http://<IP_PUBLICO_DA_EC2>:8080
```

#### 5.2.2. Método 2: Configurar /etc/hosts (Para teste local)
```bash
# Adicionar entrada no arquivo hosts local (execute na instância EC2 da AWS Academy)
echo "127.0.0.1 hello-world.local" | sudo tee -a /etc/hosts

# Testar o acesso via nome
curl http://hello-world.local
```

### 5.3. Acessar via Navegador Web

Para acessar via navegador web no seu computador local, você tem duas opções:

#### Opção A: Configurar hosts no seu computador local
1. No seu computador local (não na EC2), edite o arquivo hosts:
   - **Windows**: `C:\Windows\System32\drivers\etc\hosts`
   - **macOS/Linux**: `/etc/hosts`
2. Adicione a linha: `<IP_PUBLICO_DA_EC2> hello-world.local`
3. Acesse no navegador: `http://hello-world.local:8080`

#### Opção B: Criar um Ingress sem hostname específico
```bash
# Criar um Ingress que responde a qualquer hostname (execute na instância EC2 da AWS Academy)
cat <<EOF > ingress-wildcard.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: hello-world-ingress-wildcard
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: hello-world
            port:
              number: 8080
EOF

# Aplicar o novo Ingress
sudo kubectl apply -f ingress-wildcard.yaml

# Deletar o Ingress anterior para evitar conflitos
sudo kubectl delete ingress hello-world-ingress
```

Agora você pode acessar diretamente via: `http://<IP_PUBLICO_DA_EC2>:8080`

---

## 6. Verificação e Diagnóstico

### 6.1. Verificar Status dos Componentes
```bash
# Verificar se todos os pods estão rodando
sudo kubectl get pods -A

# Verificar especificamente o Ingress Controller
sudo kubectl get pods -n ingress-nginx

# Verificar os Ingress resources
sudo kubectl get ingress

# Verificar detalhes do Ingress
sudo kubectl describe ingress hello-world-ingress-wildcard
```

### 6.2. Verificar os Logs do Ingress Controller
```bash
# Verificar os logs do Ingress Controller
sudo kubectl logs -n ingress-nginx --tail 10 -l app.kubernetes.io/name=ingress-nginx

# Verificar eventos
sudo kubectl get events --namespace ingress-nginx

# Verificar eventos da aplicação
sudo kubectl get events --namespace default
```

### 6.3. Testes de Conectividade
```bash
# Testar conectividade interna
sudo kubectl exec -it deployment/hello-world -- curl localhost:8080

# Verificar se o serviço está acessível
sudo kubectl run test-pod --image=curlimages/curl --rm -it --restart=Never -- curl hello-world:8080

# Testar o Ingress internamente
curl -H "Host: hello-world.local" http://localhost
```

---

## 7. Testes Avançados

### 7.1. Criar Múltiplas Aplicações
```bash
# Criar uma segunda aplicação para demonstrar roteamento
sudo kubectl create deployment hello-world-v2 --image=gcr.io/google-samples/hello-app:2.0
sudo kubectl expose deployment hello-world-v2 --port=8080 --target-port=8080

# Criar Ingress com múltiplos paths
cat <<EOF > ingress-multi-path.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: multi-path-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /v1
        pathType: Prefix
        backend:
          service:
            name: hello-world
            port:
              number: 8080
      - path: /v2
        pathType: Prefix
        backend:
          service:
            name: hello-world-v2
            port:
              number: 8080
EOF

# Aplicar o novo Ingress
sudo kubectl apply -f ingress-multi-path.yaml

# Testar os diferentes paths
curl http://<IP_PUBLICO_DA_EC2>:8080/v1
curl http://<IP_PUBLICO_DA_EC2>:8080/v2
```

### 7.2. Monitoramento em Tempo Real
```bash
# Monitorar logs do Ingress em tempo real
sudo kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx -f
# Pressione Ctrl+C para parar

# Em outro terminal, faça requests para ver os logs
curl http://<IP_PUBLICO_DA_EC2>:8080/v1
curl http://<IP_PUBLICO_DA_EC2>:8080/v2
```

---

## 8. Troubleshooting

### 8.1. Problemas Comuns

**Ingress não responde:**
```bash
# Verificar se o Ingress Controller está rodando
sudo kubectl get pods -n ingress-nginx

# Verificar se há erros nos logs
sudo kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# Verificar se o Ingress foi aplicado corretamente
sudo kubectl get ingress
sudo kubectl describe ingress
```

**Aplicação não acessível via NodePort:**
```bash
# Verificar se o pod está rodando
sudo kubectl get pods

# Verificar se o serviço está configurado
sudo kubectl get svc

# Testar conectividade local
curl http://localhost:30080
```

**404 Not Found via Ingress:**
```bash
# Verificar se o serviço backend está funcionando
sudo kubectl get endpoints

# Verificar configuração do Ingress
sudo kubectl describe ingress

# Verificar logs do Ingress para erros de roteamento
sudo kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx | grep ERROR
```

### 8.2. Comandos de Diagnóstico
```bash
# Verificar configuração completa do cluster
sudo kubectl get all -A

# Verificar se o Kind cluster está saudável
sudo kubectl cluster-info

# Verificar mapeamento de portas do Kind
sudo docker ps | grep ingress-lab
```

---

## 9. Limpeza dos Recursos

```bash
# Para limpar os recursos (execute na instância EC2 da AWS Academy):
sudo kubectl delete -f ingress-multi-path.yaml
sudo kubectl delete -f ingress-wildcard.yaml
sudo kubectl delete -f ingress.yaml
sudo kubectl delete -f hello-world-nodeport.yaml
sudo kubectl delete svc hello-world hello-world-v2
sudo kubectl delete deployment hello-world hello-world-v2
sudo kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# Para remover completamente o cluster Kind:
sudo kind delete cluster --name ingress-lab
```

---

## 10. Considerações para AWS Academy

### 10.1. Security Groups
Certifique-se de que o Security Group da instância EC2 permite tráfego de entrada nas portas:
- **Porta 8080** (HTTP) para acesso via Ingress
- **Porta 30080** (HTTP) para acesso direto via NodePort
- **Porta 8443** (HTTPS) se configurar TLS

### 10.2. Diferenças do Ambiente Local
- No ambiente AWS Academy, o acesso é via IP público da EC2, não localhost
- Configurações de DNS podem requerer ajustes no arquivo hosts local
- Security Groups precisam ser configurados adequadamente

### 10.3. Monitoramento de Recursos
- O Ingress NGINX pode consumir recursos significativos
- Monitore o uso de CPU e memória da instância EC2
- Sempre limpe os recursos ao final do laboratório

---

## 11. Próximos Passos

### 11.1. Funcionalidades Avançadas
Para explorar mais funcionalidades do Ingress NGINX:

1. **TLS/SSL**: Configurar certificados para HTTPS
2. **Rate Limiting**: Implementar limitação de taxa
3. **Authentication**: Configurar autenticação básica
4. **Load Balancing**: Testar diferentes algoritmos de balanceamento

### 11.2. Integração com Outros Serviços
- **Cert-Manager**: Para certificados SSL automáticos
- **External-DNS**: Para configuração automática de DNS
- **Prometheus**: Para monitoramento de métricas do Ingress

---

Com isso, você tem um ambiente completo de Ingress NGINX funcionando no AWS Academy, acessível via IP público da EC2, com roteamento de tráfego HTTP baseado em hosts e paths, demonstrando como expor aplicações Kubernetes para acesso externo de forma controlada e escalável. 