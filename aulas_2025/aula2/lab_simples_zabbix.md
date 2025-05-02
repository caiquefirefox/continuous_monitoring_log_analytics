# Laboratório Simples: Zabbix com Docker

Este laboratório demonstra rapidamente como configurar o Zabbix e criar um alerta básico.

## Passo 1: Configuração do ambiente

Crie um arquivo `docker-compose.yml` com o seguinte conteúdo:

```yaml
version: '3'

services:
  zabbix-db:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_DATABASE: zabbix
      MYSQL_USER: zabbix
      MYSQL_PASSWORD: zabbix
      MYSQL_ROOT_PASSWORD: zabbix_root_pwd
    volumes:
      - mysql-data:/var/lib/mysql
    command: --default-authentication-plugin=mysql_native_password --character-set-server=utf8 --collation-server=utf8_bin

  zabbix-server:
    image: zabbix/zabbix-server-mysql:ubuntu-6.0-latest
    restart: always
    ports:
      - "10051:10051"
    environment:
      DB_SERVER_HOST: zabbix-db
      MYSQL_DATABASE: zabbix
      MYSQL_USER: zabbix
      MYSQL_PASSWORD: zabbix
    depends_on:
      - zabbix-db

  zabbix-web:
    image: zabbix/zabbix-web-nginx-mysql:ubuntu-6.0-latest
    restart: always
    ports:
      - "8080:8080"
    environment:
      DB_SERVER_HOST: zabbix-db
      MYSQL_DATABASE: zabbix
      MYSQL_USER: zabbix
      MYSQL_PASSWORD: zabbix
      ZBX_SERVER_HOST: zabbix-server
      PHP_TZ: America/Sao_Paulo
    depends_on:
      - zabbix-db
      - zabbix-server

  zabbix-agent:
    image: zabbix/zabbix-agent2:ubuntu-6.0-latest
    restart: always
    privileged: true
    environment:
      ZBX_HOSTNAME: "Lab-Docker-Agent"
      ZBX_SERVER_HOST: zabbix-server
    depends_on:
      - zabbix-server

volumes:
  mysql-data:
```

Execute o ambiente Docker:

```bash
docker-compose up -d
```

## Passo 2: Acesse o Zabbix

1. Abra o navegador: http://localhost:8080
2. Login: Admin / Senha: zabbix

## Passo 3: Configure um host

1. Vá para **Configuration** → **Hosts**
2. Clique em **Create host**
3. Configure:
   - Host name: `Lab-Docker-Agent`
   - Groups: Selecione `Linux servers`
   - Interfaces: Tipo Agent, IP `zabbix-agent`, porta `10050`
4. Vá para a aba **Templates**
5. Adicione o template `Linux by Zabbix agent`
6. Clique em **Add**

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
   - Expression: `{Lab-Docker-Agent:system.cpu.util[,user].last()}>20`
8. Clique em **Add**

## Passo 5: Teste o alerta

Execute no terminal:

```bash
docker-compose exec zabbix-agent bash -c "apt-get update && apt-get install -y stress && stress -c 2 -t 60"
```

Vá para **Monitoring** → **Problems** para ver o alerta aparecer.

## Passo 6: Encerre o ambiente

Quando terminar:

```bash
docker-compose down
``` 