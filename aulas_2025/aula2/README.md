# Laboratório Simples: Zabbix com Docker

Este laboratório demonstra rapidamente como configurar o Zabbix e criar um alerta básico.

## Passo 1: Configuração do ambiente

O arquivo `docker-compose.yml` já está configurado. Execute:

```bash
# Primeiro, limpe qualquer instalação anterior
docker-compose down -v

# Inicie os containers
docker-compose up -d
```

Aguarde aproximadamente 1-2 minutos para que todos os serviços iniciem corretamente. Você pode verificar o status dos containers com:

```bash
docker ps
```

Todos os 4 containers (zabbix-db, zabbix-server, zabbix-web e zabbix-agent) devem estar em execução.

## Passo 2: Acesse o Zabbix

1. Abra o navegador: http://localhost:8080
2. Login: Admin / Senha: zabbix

## Passo 3: Configure um host

### Se você precisa editar um host existente:

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
       docker inspect aula2-zabbix-agent-1 | grep IPAddress
       ```
     - Porta: `10050`
     - Importante: Marque a opção "Connect to" como DNS se usar o nome do serviço, ou IP se usar o endereço IP
   - Verifique se os templates apropriados estão aplicados (veja a seção "Para criar um novo host" abaixo)
5. Clique em **Update** para salvar as alterações

### Para criar um novo host:

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
     docker inspect aula2-zabbix-agent-1 | grep IPAddress
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

## Passo 4: Crie um alerta simples

1. Vá para o host criado e acesse a aba **Items**
2. Clique em **Create item**
3. Configure:
   - Name: `CPU Teste`
   - Key: `system.cpu.util[,user]`
   - Type of information: `Numeric (float)`
   - Units: `%`
4. Clique em **Add**

5. Vá para a aba **Triggers**
6. Clique em **Create trigger**
7. Configure:
   - Name: `CPU alta em {HOST.NAME}`
   - Severity: `Warning`
   - Expressão: Digite diretamente no campo expression:
     ```
     last(/Lab-Docker-Agent/system.cpu.util[,user])>20
     ```
8. Clique em **Add** para salvar o trigger

## Passo 5: Teste o alerta

**Nota importante**: O template "Linux by Zabbix agent" já vem com alguns alertas pré-configurados, como o alerta de uso de swap. É normal ver um alerta como "High swap space usage" mesmo sem realizar testes adicionais.

### Método 1: Usando o container do agente
Se possível, execute no terminal:

```bash
# Usando o nome exato do container, não o serviço
docker exec -it aula2-zabbix-agent-1 bash -c "apt-get update && apt-get install -y stress && stress -c 2 -t 60"
```

### Método 2: Alternativa no host (se o método 1 falhar)
Se o método 1 não funcionar, execute este comando diretamente no host para gerar carga de CPU:

```bash
# Gera carga de CPU por 60 segundos
for i in {1..8}; do yes > /dev/null & done; sleep 60; pkill yes
```

Vá para **Monitoring** → **Problems** para ver o alerta aparecer. Você provavelmente verá alertas relacionados à CPU ou outros recursos, como o de uso de swap.

## Passo 6: Encerre o ambiente

Quando terminar:

```bash
docker-compose down
```

Para remover também os volumes persistentes (apaga todos os dados):

```bash
docker-compose down -v
```

## Solução de problemas

Se você encontrar algum problema, tente:

1. Verificar se todos os containers estão rodando:
   ```bash
   docker ps
   ```

2. Verificar os logs dos containers:
   ```bash
   docker-compose logs zabbix-server
   docker-compose logs zabbix-agent
   ```

3. Testar a comunicação entre o servidor e o agente:
   ```bash
   # Testando com o nome do serviço (DNS)
   docker exec -it aula2-zabbix-server-1 zabbix_get -s zabbix-agent -p 10050 -k agent.ping
   
   # Ou com o IP do agente
   IP_AGENTE=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' aula2-zabbix-agent-1)
   docker exec -it aula2-zabbix-server-1 zabbix_get -s $IP_AGENTE -p 10050 -k agent.ping
   ```
   
   O resultado deve ser: `1`

4. Verificar as portas expostas:
   ```bash
   docker-compose ps
   ```
   
   Confirme que as portas 8080 (web) e 10050 (agent) estão mapeadas corretamente.

5. Reiniciar os containers:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

6. Importante: Se você estiver enfrentando problemas com comandos docker-compose, tente usar o nome completo do container em vez do serviço:
   ```bash
   # Em vez de:
   docker-compose exec zabbix-agent comando
   
   # Use:
   docker exec -it aula2-zabbix-agent-1 comando
   ``` 