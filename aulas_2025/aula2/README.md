# Laboratório Atualizado: Zabbix com Docker - AWS Academy

Este laboratório demonstra rapidamente como configurar o Zabbix e criar um alerta básico no ambiente AWS Academy.

✅ **Data da Atualização: 21 de Maio de 2025**

---

## Passo 1: Configuração do ambiente

### 1.1. Baixar o arquivo de configuração
O arquivo `docker-compose.yml` já está configurado. Execute na instância EC2 da AWS Academy:

```bash
# Execute na instância EC2 da AWS Academy
wget https://raw.githubusercontent.com/able2cloud/continuous_monitoring_log_analytics/refs/heads/main/aulas_2025/aula2/docker-compose.yml
```

### 1.2. Configurar o Docker Compose
Primeiro, certifique-se de que o Docker está instalado e funcionando:

```bash
# Verificar se o Docker está rodando
sudo systemctl status docker

# Se não estiver instalado, instale o Docker (apenas se necessário)
sudo apt-get update
sudo apt-get install docker.io docker-compose-plugin -y
sudo usermod -aG docker $USER
newgrp docker
```

### 1.3. Iniciar os containers
```bash
# Primeiro, limpe qualquer instalação anterior
sudo docker compose down -v

# Inicie os containers (execute na instância EC2 da AWS Academy)
sudo docker compose up -d
```

Aguarde aproximadamente 2-3 minutos para que todos os serviços iniciem corretamente. Você pode verificar o status dos containers com:

```bash
sudo docker ps
```

Todos os 4 containers (zabbix-db, zabbix-server, zabbix-web e zabbix-agent) devem estar em execução.

---

## Passo 2: Acesse o Zabbix

### 2.1. Configurar acesso via IP público
**No ambiente AWS Academy, acesse via navegador:**
```
http://<IP_PUBLICO_DA_EC2>:8080
```

**Onde:**
- `<IP_PUBLICO_DA_EC2>` deve ser substituído pelo endereço IP público da sua instância EC2 da AWS Academy
- A porta `8080` está mapeada no docker-compose para acesso externo

**Para encontrar o IP público da sua instância EC2:**
1. Acesse o console da AWS Academy
2. Vá para EC2 > Instances  
3. Localize sua instância e copie o "Public IPv4 address"

**Importante:** Certifique-se de que o Security Group da instância EC2 permite tráfego de entrada na porta 8080.

### 2.2. Fazer login
- **Login:** Admin
- **Senha:** zabbix

---

## Passo 3: Configure um host

### 3.1. Se você precisa editar um host existente:

1. Vá para **Configuration** → **Hosts**
2. Localize o host existente (pode estar com nome "zabbix-server" ou outro nome)
3. Clique no nome do host para editar
4. Corrija as configurações:
   - Host name: Altere para `Lab-Docker-Agent` (exatamente como escrito aqui)
   - Remova qualquer interface configurada incorretamente (especialmente se estiver usando 127.0.0.1)
   - Adicione uma nova interface Agent (ou edite a existente):
     - Tipo: Agent
     - IP: Use `zabbix-agent` (nome do serviço) ou obtenha o IP do container com:
       ```bash
       sudo docker inspect aula2-zabbix-agent-1 | grep IPAddress
       ```
     - Porta: `10050`
     - Importante: Marque a opção "Connect to" como DNS se usar o nome do serviço, ou IP se usar o endereço IP
   - Verifique se os templates apropriados estão aplicados (veja a seção "Para criar um novo host" abaixo)
5. Clique em **Update** para salvar as alterações

### 3.2. Para criar um novo host:

1. Vá para **Configuration** → **Hosts**
2. Clique em **Create host**
3. Configure:
   - Host name: `Lab-Docker-Agent`
   - Visible name: `Lab-Docker-Agent` (opcional)
   - Groups: Selecione `Linux servers`

4. É necessário adicionar uma interface Agent clicando no botão **Add** na seção "Interfaces":
   - Tipo: Agent
   - IP: Use `zabbix-agent` (nome do serviço) ou obtenha o IP do container com:
     ```bash
     sudo docker inspect aula2-zabbix-agent-1 | grep IPAddress
     ```
   - Porta: `10050`
   - Importante: Marque a opção "Connect to" como DNS se usar o nome do serviço, ou IP se usar o endereço IP
   - Mantenha a opção "Default" selecionada
   - Clique em "Add" para adicionar a interface

5. Ainda na mesma tela de criação do host, vá para a aba **Templates** (que aparece na parte superior do formulário)
6. No campo de busca de templates, digite `Linux by Zabbix agent` e selecione este template quando aparecer
7. Clique no botão **Add** no final da página para salvar toda a configuração do host

8. **Verificação**: Após adicionar ou editar o host, aguarde 1-2 minutos e depois:
   - Vá para **Monitoring** → **Latest data**
   - Filtre por host: `Lab-Docker-Agent`
   - Você deverá ver dados como uso de CPU, memória, etc. chegando do agente
   - Se o status da interface do agente estiver como "Unknown", aguarde mais alguns minutos

---

## Passo 4: Crie um alerta simples

### 4.1. Criar um item personalizado
1. Vá para o host criado e acesse a aba **Items**
2. Clique em **Create item**
3. Configure:
   - Name: `CPU Teste`
   - Key: `system.cpu.util[,user]`
   - Type of information: `Numeric (float)`
   - Units: `%`
4. Clique em **Add**

### 4.2. Criar um trigger
1. Vá para a aba **Triggers**
2. Clique em **Create trigger**
3. Configure:
   - Name: `CPU alta em {HOST.NAME}`
   - Severity: `Warning`
   - Expressão: Digite diretamente no campo expression:
     ```
     last(/Lab-Docker-Agent/system.cpu.util[,user])>20
     ```
4. Clique em **Add** para salvar o trigger

---

## Passo 5: Teste o alerta

**Nota importante**: O template "Linux by Zabbix agent" já vem com alguns alertas pré-configurados, como o alerta de uso de swap. É normal ver um alerta como "High swap space usage" mesmo sem realizar testes adicionais.

### 5.1. Método 1: Usando o container do agente
Se possível, execute no terminal da instância EC2 da AWS Academy:

```bash
# Usando o nome exato do container, não o serviço (execute na instância EC2 da AWS Academy)
sudo docker exec -it aula2-zabbix-agent-1 bash -c "apt-get update && apt-get install -y stress && stress -c 2 -t 60"
```

### 5.2. Método 2: Alternativa no host (se o método 1 falhar)
Se o método 1 não funcionar, execute este comando diretamente na instância EC2 da AWS Academy para gerar carga de CPU:

```bash
# Gera carga de CPU por 60 segundos na instância EC2 da AWS Academy
for i in {1..8}; do yes > /dev/null & done; sleep 60; pkill yes
```

### 5.3. Verificar os alertas
Vá para **Monitoring** → **Problems** para ver o alerta aparecer. Você provavelmente verá alertas relacionados à CPU ou outros recursos, como o de uso de swap.

**Observação:** Podem levar alguns minutos para os alertas aparecerem no dashboard, pois o Zabbix coleta dados em intervalos regulares.

---

## Passo 6: Verificação adicional do funcionamento

### 6.1. Verificar métricas em tempo real
1. Vá para **Monitoring** → **Latest data**
2. Filtre por host: `Lab-Docker-Agent`  
3. Observe as métricas sendo coletadas em tempo real
4. Durante o teste de carga, você deve ver o aumento no uso de CPU

### 6.2. Verificar gráficos
1. Vá para **Monitoring** → **Graphs**
2. Selecione o host `Lab-Docker-Agent`
3. Escolha gráficos como "CPU utilization" para visualizar as tendências

---

## Passo 7: Encerre o ambiente

Quando terminar:

```bash
# Execute na instância EC2 da AWS Academy
sudo docker compose down
```

Para remover também os volumes persistentes (apaga todos os dados):

```bash
# Execute na instância EC2 da AWS Academy  
sudo docker compose down -v
```

---

## Solução de problemas

Se você encontrar algum problema, tente:

### 7.1. Verificações básicas
```bash
# 1. Verificar se todos os containers estão rodando
sudo docker ps

# 2. Verificar os logs dos containers
sudo docker compose logs zabbix-server
sudo docker compose logs zabbix-agent

# 3. Verificar se o Docker está rodando
sudo systemctl status docker
```

### 7.2. Testes de conectividade
```bash
# 4. Testar a comunicação entre o servidor e o agente
# Testando com o nome do serviço (DNS)
sudo docker exec -it aula2-zabbix-server-1 zabbix_get -s zabbix-agent -p 10050 -k agent.ping

# Ou com o IP do agente
IP_AGENTE=$(sudo docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' aula2-zabbix-agent-1)
sudo docker exec -it aula2-zabbix-server-1 zabbix_get -s $IP_AGENTE -p 10050 -k agent.ping
```

O resultado deve ser: `1`

### 7.3. Verificações de rede
```bash
# 5. Verificar as portas expostas
sudo docker compose ps

# 6. Testar acesso local ao Zabbix web
curl -I http://localhost:8080
```

Confirme que as portas 8080 (web) e 10050 (agent) estão mapeadas corretamente.

### 7.4. Reinicialização
```bash
# 7. Reiniciar os containers se necessário
sudo docker compose down
sudo docker compose up -d

# Aguarde 2-3 minutos para todos os serviços subirem completamente
```

### 7.5. Problemas de Security Group
**Se não conseguir acessar via IP público:**
- Verifique se o Security Group da instância EC2 permite tráfego de entrada na porta 8080
- Teste primeiro o acesso local: `curl http://localhost:8080`
- Confirme que o IP público da EC2 está correto

### 7.6. Problemas com nomes de containers
Se você estiver enfrentando problemas com comandos docker-compose, tente usar o nome completo do container em vez do serviço:

```bash
# Em vez de:
sudo docker compose exec zabbix-agent comando

# Use:
sudo docker exec -it aula2-zabbix-agent-1 comando
```

---

**Importante para AWS Academy:**
- Certifique-se de que o Security Group permite tráfego HTTP na porta 8080
- Use o IP público da instância EC2 para acessar o Zabbix
- Todos os comandos devem ser executados com `sudo` na instância EC2
- O ambiente deve ser limpo ao final para evitar custos desnecessários
