# 🎨 Exercício Adicional: Pods Coloridos com Informações

## 📋 Pré-requisitos
- Cluster Kind funcionando (conforme README.md principal)
- Kubernetes Dashboard acessível
- httpbin já implantado (exercício anterior)

✅ **Exercício Complementar - Complexidade: Simples**

---

## 🎯 Objetivo do Exercício

Implantar uma aplicação que mostra informações únicas de cada pod, permitindo visualizar conceitos importantes do Kubernetes de forma prática e visual através do Dashboard.

### O que você vai aprender:
- 🔍 Cada pod é único (hostname, IP)
- ⚖️ Load balancing entre pods
- 📈 Scaling horizontal em tempo real
- 🔄 Rolling updates com progresso visual
- 📊 Monitoramento via Dashboard

---

## 🚀 Parte 1: Deploy da Aplicação "WhoAmI"

### 1.1. Criar o Deployment
```bash
# Criar um deployment simples mas interessante
cat > whoami-app.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: whoami-deployment
  labels:
    app: whoami
spec:
  replicas: 3
  selector:
    matchLabels:
      app: whoami
  template:
    metadata:
      labels:
        app: whoami
    spec:
      containers:
      - name: whoami
        image: traefik/whoami:latest
        ports:
        - containerPort: 80
        env:
        - name: WHOAMI_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
---
apiVersion: v1
kind: Service
metadata:
  name: whoami-service
spec:
  type: NodePort
  selector:
    app: whoami
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
    nodePort: 30095
EOF
```

### 1.2. Aplicar a Configuração
```bash
# Aplicar o deployment
sudo kubectl apply -f whoami-app.yaml

# Verificar se os pods estão rodando
sudo kubectl get pods -l app=whoami

# Verificar o serviço
sudo kubectl get svc whoami-service
```

> 💡 **Dica:** Aguarde todos os pods ficarem em estado "Running" antes de prosseguir.

---

## 👀 Parte 2: Atividades no Dashboard

### 🔍 Atividade 1: Explorar os 3 Pods Diferentes

**No Kubernetes Dashboard:**

1. 📊 Navegue até `Workloads` → `Pods`
2. 🔍 Procure pelos pods que começam com `whoami-deployment-`
3. 📋 Clique em cada pod individualmente
4. 📝 Na aba `Logs`, observe as informações únicas de cada pod

**O que você deve ver:**
- Hostname diferente para cada pod
- IP interno único
- Informações específicas do container

**Teste via linha de comando:**
```bash
# Acesse várias vezes e veja pods diferentes respondendo
curl http://localhost:30095
curl http://localhost:30095
curl http://localhost:30095
```

> 💡 **Interessante:** Cada requisição pode ser atendida por um pod diferente!

### 📈 Atividade 2: Scaling Visual

**Scale UP no Dashboard:**

1. 📊 Vá em `Workloads` → `Deployments` → `whoami-deployment`
2. 🔧 Clique no ícone "Scale" (ícone com setas)
3. 📈 Mude para **6 réplicas**
4. 👀 **Observe:** Novos pods aparecendo em tempo real na seção `Pods`!

**Scale DOWN:**
1. 📉 Diminua para **2 réplicas**
2. 👀 **Veja:** Pods sendo terminados gradualmente

**Comandos alternativos via CLI:**
```bash
# Scale via comando
sudo kubectl scale deployment whoami-deployment --replicas=6

# Verificar o scaling
sudo kubectl get pods -l app=whoami --watch
```

### 🔄 Atividade 3: Rolling Update Simples

```bash
# Simular uma atualização da imagem
sudo kubectl set image deployment/whoami-deployment whoami=traefik/whoami:v1.8.0
```

**No Dashboard (faça rapidamente após o comando):**
1. 📊 Vá em `Workloads` → `Deployments` → `whoami-deployment`
2. 👀 **Observe:** A barra de progresso da atualização!
3. 📋 Vá em `Workloads` → `Pods` para ver pods sendo recriados

**O que observar:**
- Pods antigos sendo terminados
- Pods novos sendo criados
- Status da atualização em tempo real

### 📊 Atividade 4: Informações Detalhadas dos Pods

**Para cada pod no Dashboard, explore as abas:**

1. 📝 **Aba Overview:** 
   - Nome do pod
   - Status atual
   - IP interno do pod
   - Node onde está rodando

2. 📜 **Aba Logs:** 
   - Informações únicas do container
   - Hostname específico
   - Requisições recebidas

3. 📅 **Aba Events:** 
   - Histórico do que aconteceu com o pod
   - Criação, inicialização, etc.

4. 🔧 **Aba YAML:** 
   - Configuração completa do pod
   - Variáveis de ambiente
   - Configurações do container

---

## 🌐 Parte 3: Teste Visual de Load Balancing

### 3.1. Script de Teste Automático
```bash
# Script para fazer múltiplas requisições e ver o balanceamento
for i in {1..10}; do
  echo "Requisição $i:"
  curl -s http://localhost:30095 | grep -E "(Hostname|IP)"
  echo "---"
  sleep 1
done
```

### 3.2. Teste Manual
```bash
# Teste individual
curl http://localhost:30095

# Teste via IP público (se configurado)
curl http://<IP_PUBLICO_DA_EC2>:30095
```

**Resultado Esperado:**
- Hostnames diferentes aparecem aleatoriamente
- IPs internos variados
- Demonstra o load balancing funcionando

---

## 🌐 Parte 4: Acesso via Navegador

### 4.1. Acesso Local (na EC2)
```
http://localhost:30095
```

### 4.2. Acesso Externo (do seu computador)
```
http://<IP_PUBLICO_DA_EC2>:30095
```

> ⚠️ **Lembre-se:** Libere a porta 30095 no Security Group se quiser acesso externo!

**O que você verá no navegador:**
```
Hostname: whoami-deployment-xxxxx-xxxxx
IP: 10.244.0.x
RemoteAddr: x.x.x.x:xxxxx
GET / HTTP/1.1
Host: <IP>:30095
User-Agent: Mozilla/5.0...
```

---

## 🎓 Parte 5: Perguntas de Reflexão

### 🤔 Para pensar e discutir:

1. **Load Balancing:** Por que cada requisição pode ser atendida por um pod diferente?

2. **Scaling:** O que acontece com as conexões ativas quando você faz scale down?

3. **Rolling Update:** Por que o Kubernetes não para todos os pods de uma vez durante a atualização?

4. **Uniqueness:** O que torna cada pod único no cluster?

5. **Service:** Como o serviço NodePort distribui as requisições entre os pods?

---

## 📊 Parte 6: Comparação com httpbin

### Diferenças Observáveis:

| Aspecto | httpbin | whoami |
|---------|---------|---------|
| **Função** | API de teste HTTP | Mostra informações do pod |
| **Complexidade** | Mais recursos | Simples e direto |
| **Visualização** | JSON estruturado | Texto simples |
| **Uso** | Testes de API | Demonstração de conceitos |

### Similaridades:
- ✅ Ambos usam NodePort
- ✅ Demonstram load balancing
- ✅ Permitem scaling
- ✅ São visíveis no Dashboard

---

## 🧹 Limpeza dos Recursos

```bash
# Remover a aplicação whoami
sudo kubectl delete -f whoami-app.yaml

# Verificar se foi removido
sudo kubectl get pods -l app=whoami
sudo kubectl get svc whoami-service
```

> 💡 **Nota:** Os comandos devem retornar "No resources found" após a limpeza.

---

## 🎯 Resumo do Aprendizado

### ✅ O que você praticou:

- 🔧 **Deploy simples** com configuração YAML
- 👀 **Visualização no Dashboard** de múltiplos pods
- 📈 **Scaling horizontal** em tempo real
- 🔄 **Rolling updates** com progresso visual
- 🌐 **Load balancing** entre pods
- 📊 **Monitoramento** via Dashboard

### 🎨 Por que este exercício é interessante:

- 🎯 **Visual:** Cada pod mostra informações diferentes
- ⚡ **Rápido:** Menos de 5 minutos para completar
- 🎮 **Interativo:** Scale up/down em tempo real
- 📱 **Prático:** Conceitos fundamentais do Kubernetes

---

## 🚀 Próximos Passos Sugeridos

Agora que você dominou os conceitos básicos, pode explorar:

1. 🔍 **Logs em tempo real** de múltiplos pods
2. 📊 **Métricas de recursos** (CPU/Memória)
3. 🔧 **ConfigMaps e Secrets** (exercício mais avançado)
4. 🌐 **Ingress Controllers** para roteamento
5. 💾 **Persistent Volumes** para armazenamento

---

**🎉 Parabéns!** Você completou o exercício adicional do Kubernetes Dashboard!

> 💡 **Dica Final:** Use este conhecimento para explorar outros deployments mais complexos no Dashboard! 