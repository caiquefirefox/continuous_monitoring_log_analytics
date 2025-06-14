# 🚀 ELK Stack 2025 - Lab Aula 7

## Monitoramento Avançado de Logs com Elasticsearch, Logstash e Kibana

---

## 📋 **Pré-requisitos**
- Docker 20.0+ instalado
- Docker Compose 2.0+ instalado  
- 6GB+ de RAM disponível
- 5GB+ de espaço em disco

---

## 🔧 **Passo 1: Instalar Docker Compose (se necessário)**

```bash
# Instalar Docker Compose
sudo apt update
sudo apt install -y docker-compose

# Verificar instalação
docker-compose --version
```

---

## 📥 **Passo 2: Clone o Repositório** 

```bash
# Clone o repositório do curso
git clone https://github.com/able2cloud/continuous_monitoring_log_analytics.git

# Entre no diretório da aula 7
cd continuous_monitoring_log_analytics/aulas_2025/aula7
```

---

## 🚀 **Passo 3: Execute o Script Automático**

```bash
# Torne o script executável e execute
chmod +x start.sh
./start.sh
```

**O script irá automaticamente:**
- ✅ Verificar pré-requisitos
- ✅ Configurar o sistema
- ✅ Baixar imagens Docker
- ✅ Iniciar todos os serviços
- ✅ Gerar logs de teste

---

## 🌐 **Passo 4: Acesse as Interfaces**

- **Aplicação Web**: http://`<IP_PUBLICO_DA_EC2>` *(gere logs aqui)*
- **Kibana**: http://`<IP_PUBLICO_DA_EC2>`:5601 *(visualize os dados)*
- **Elasticsearch**: http://`<IP_PUBLICO_DA_EC2>`:9200 *(API de dados)*

---

## 🔧 **Como o Nginx Funciona Neste Lab**

### **Configuração Automática**
O Nginx é automaticamente configurado pelo Docker Compose com:

- **Logs em formato JSON** - Para facilitar o parsing
- **Interface web interativa** - Para gerar logs de teste
- **Endpoints de monitoramento** - Para health checks

### **Estrutura dos Logs**
O Nginx gera logs estruturados em JSON com campos importantes:
```json
{
  "time_local": "25/Dec/2025:10:30:45 +0000",
  "remote_addr": "172.17.0.1",
  "status": "200",
  "request_time": "0.001",
  "http_user_agent": "Mozilla/5.0...",
  "request": "GET / HTTP/1.1"
}
```

### **Fluxo dos Logs**
```
Nginx → Logs JSON → Filebeat/Logstash → Elasticsearch → Kibana
```

---

## 🎯 **Passo 5: Gerar Logs de Teste**

**Acesse**: http://`<IP_PUBLICO_DA_EC2>`

Use os botões da interface:
- ✅ **Sucesso (200)** - Requisições OK
- ❌ **Erro 404** - Páginas não encontradas  
- 💥 **Erro 500** - Erros de servidor
- 🚀 **Múltiplas Requisições** - Teste de volume

---

## 🔍 **Passo 6: Inserir Logs e Visualizar**

### **A. Inserir logs de exemplo:**
```bash
# Inserir logs via API
curl -X POST "localhost:9200/logstash-nginx-$(date +%Y.%m.%d)/_doc" \
-H "Content-Type: application/json" \
-d '{
  "@timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
  "remote_addr": "192.168.1.100",
  "status": "200",
  "request": "GET / HTTP/1.1",
  "request_time": "0.001",
  "http_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}'

curl -X POST "localhost:9200/logstash-nginx-$(date +%Y.%m.%d)/_doc" \
-H "Content-Type: application/json" \
-d '{
  "@timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
  "remote_addr": "10.0.0.1",
  "status": "404",
  "request": "GET /test HTTP/1.1",
  "request_time": "0.002",
  "http_user_agent": "curl/7.68.0"
}'

curl -X POST "localhost:9200/logstash-nginx-$(date +%Y.%m.%d)/_doc" \
-H "Content-Type: application/json" \
-d '{
  "@timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)'",
  "remote_addr": "203.0.113.15",
  "status": "500",
  "request": "POST /api/users HTTP/1.1",
  "request_time": "1.234",
  "http_user_agent": "PostmanRuntime/7.28.4"
}'
```

### **B. Criar data view:**
```bash
curl -X POST "localhost:5601/api/data_views/data_view" \
-H "kbn-xsrf: true" \
-H "Content-Type: application/json" \
-d '{
  "data_view": {
    "title": "logstash-nginx-*",
    "timeFieldName": "@timestamp"
  }
}'
```

### **C. Visualizar no Kibana:**
1. **Acesse**: http://`<IP_PUBLICO_DA_EC2>`:5601
2. **Vá para**: Discover
3. **Selecione**: `logstash-nginx-*`
4. **Pronto!** Os logs aparecerão.

---

## 🛠️ **Comandos Úteis**

```bash
# Ver status dos serviços
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f

# Parar tudo
docker-compose down

# Reiniciar
docker-compose restart
```

---

## 🐛 **Problemas Comuns**

**Elasticsearch não inicia:**
```bash
sudo sysctl -w vm.max_map_count=262144
```

**Verificar se tudo está funcionando:**
```bash
curl http://localhost:9200/_cluster/health
curl http://localhost:5601/api/status
```

---

**🎓 Desenvolvido para fins educacionais - Able2Cloud 2025** 