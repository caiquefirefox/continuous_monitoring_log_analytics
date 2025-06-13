# 🚀 ELK Stack 2025 - Lab Aula 7

## Monitoramento Avançado de Logs com Elasticsearch, Logstash e Kibana

Este laboratório apresenta uma implementação moderna e completa da stack ELK (Elasticsearch, Logstash, Kibana) com melhorias significativas em relação à versão de 2023.

---

## 🆕 **Novidades da Versão 2025**

### ✨ **Principais Melhorias**
- **ELK Stack 8.11.3** - Versões mais recentes com melhor performance
- **Logs Estruturados JSON** - Nginx configurado para logs JSON nativos
- **Filebeat & Metricbeat** - Coleta moderna de logs e métricas
- **Health Checks** - Monitoramento de saúde de todos os serviços
- **Interface Web Interativa** - Gerador de logs para testes
- **Configurações Otimizadas** - Performance e segurança aprimoradas
- **GeoIP & User Agent Parsing** - Enriquecimento automático de dados
- **Dashboards Pré-configurados** - Visualizações prontas para uso

---

## 🏗️ **Arquitetura**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Nginx    │───▶│  Filebeat   │───▶│  Logstash   │───▶│Elasticsearch│
│(Logs JSON) │    │(Coleta Logs)│    │(Processa)   │    │(Armazena)   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                  │
┌─────────────┐    ┌─────────────┐                               │
│  Metricbeat │───▶│Elasticsearch│◀─────────────────────────────┘
│(Métricas)   │    │             │
└─────────────┘    └─────────────┘
                           │
                           ▼
                   ┌─────────────┐
                   │   Kibana    │
                   │(Visualiza)  │
                   └─────────────┘
```

---

## 🚀 **Quick Start**

### **Pré-requisitos**
- Docker 24.0+
- Docker Compose 2.0+
- 8GB RAM mínimo
- 5GB espaço em disco

### **1. Clone e Execute**
```bash
git clone https://github.com/able2cloud/continuous_monitoring_log_analytics.git
cd continuous_monitoring_log_analytics/aulas_2025/aula7

# Inicie a stack
docker-compose up -d

# Acompanhe os logs
docker-compose logs -f
```

### **2. Aguarde a Inicialização**
```bash
# Verifique o status dos serviços
docker-compose ps

# Aguarde todos ficarem 'healthy'
watch docker-compose ps
```

### **3. Acesse as Interfaces**
- **🌐 Web App**: http://localhost
- **📊 Kibana**: http://localhost:5601
- **🔍 Elasticsearch**: http://localhost:9200
- **⚙️ Logstash**: http://localhost:9600

---

## 📊 **Configuração do Kibana**

### **1. Configurar Index Patterns**
1. Acesse Kibana em http://localhost:5601
2. Vá para **Stack Management** → **Index Patterns**
3. Clique em **Create index pattern**
4. Configure os seguintes patterns:

#### **Para Logs do Nginx (via Logstash)**
- **Index pattern**: `logstash-nginx-*`
- **Time field**: `@timestamp`

#### **Para Logs do Nginx (via Filebeat)**
- **Index pattern**: `filebeat-nginx-*`
- **Time field**: `@timestamp`

#### **Para Métricas do Sistema**
- **Index pattern**: `metricbeat-*`
- **Time field**: `@timestamp`

### **2. Explorar os Dados**
1. Vá para **Discover**
2. Selecione o index pattern desejado
3. Explore os campos disponíveis:
   - `remote_addr` - IP do cliente
   - `status` - Código HTTP
   - `request_time` - Tempo de resposta
   - `geoip.*` - Localização geográfica
   - `useragent.*` - Informações do browser

---

## 🎯 **Gerando Logs de Teste**

### **Via Interface Web**
1. Acesse http://localhost
2. Use os botões de **Gerador de Logs**:
   - ✅ **Sucesso (200)** - Requisições bem-sucedidas
   - ❌ **Não Encontrado (404)** - Páginas inexistentes
   - 💥 **Erro Servidor (500)** - Erros internos
   - 🔌 **API Call** - Chamadas de API
   - 🐌 **Requisição Lenta** - Teste de performance
   - 🚀 **Múltiplas Requisições** - Teste de volume

### **Via Linha de Comando**
```bash
# Gerar tráfego variado
for i in {1..100}; do
  curl http://localhost/
  curl http://localhost/api/users
  curl http://localhost/nonexistent-page
  sleep 1
done

# Simular diferentes IPs
curl -H "X-Forwarded-For: 192.168.1.100" http://localhost/
curl -H "X-Forwarded-For: 10.0.0.50" http://localhost/
```

---

## 📈 **Criando Visualizações**

### **1. Gráfico de Status HTTP**
1. Vá para **Visualize** → **Create visualization**
2. Escolha **Pie chart**
3. Configure:
   - **Buckets**: Split slices
   - **Aggregation**: Terms
   - **Field**: `status.keyword`

### **2. Mapa de Localização de IPs**
1. Escolha **Maps**
2. Configure:
   - **Layer**: Documents
   - **Index pattern**: `logstash-nginx-*`
   - **Geospatial field**: `geoip.location`

### **3. Timeline de Requisições**
1. Escolha **Line chart**
2. Configure:
   - **X-axis**: Date Histogram (`@timestamp`)
   - **Y-axis**: Count

---

## 🔧 **Configurações Avançadas**

### **Elasticsearch**
```yaml
# Configurações de performance
ES_JAVA_OPTS: "-Xms2g -Xmx2g"
bootstrap.memory_lock: true
```

### **Logstash**
```yaml
# Pipeline otimizado
pipeline.workers: 2
pipeline.batch.size: 1000
pipeline.batch.delay: 50
```

### **Nginx Logs JSON**
O Nginx está configurado para gerar logs estruturados em JSON:
```json
{
  "time_local": "25/Dec/2025:10:30:45 +0000",
  "remote_addr": "172.17.0.1",
  "status": "200",
  "request_time": "0.001",
  "http_user_agent": "Mozilla/5.0...",
  "geoip": {...},
  "useragent": {...}
}
```

---

## 🐛 **Troubleshooting**

### **Problemas Comuns**

#### **Elasticsearch não inicia**
```bash
# Verificar recursos
docker stats

# Aumentar memória virtual
sudo sysctl -w vm.max_map_count=262144
echo 'vm.max_map_count=262144' | sudo tee -a /etc/sysctl.conf
```

#### **Logs não aparecem no Kibana**
```bash
# Verificar se Logstash está processando
curl http://localhost:9600/_node/stats/pipelines

# Verificar índices no Elasticsearch
curl http://localhost:9200/_cat/indices?v
```

#### **Health checks falhando**
```bash
# Verificar status detalhado
docker-compose exec elasticsearch curl http://localhost:9200/_cluster/health?pretty
docker-compose exec kibana curl http://localhost:5601/api/status
```

---

## 📚 **Exercícios Práticos**

### **Nível Básico**
1. Configure os index patterns no Kibana
2. Explore os logs na aba Discover
3. Crie uma visualização de pizza com status HTTP
4. Gere diferentes tipos de logs via interface web

### **Nível Intermediário**
1. Crie um dashboard com múltiplas visualizações
2. Configure alertas para erros 5xx
3. Analise padrões de user agents
4. Crie filtros por localização geográfica

### **Nível Avançado**
1. Implemente parsing customizado no Logstash
2. Configure machine learning para detecção de anomalias
3. Integre com sistemas de monitoramento externos
4. Otimize performance para alto volume de logs

---

## 🔍 **Monitoramento e Métricas**

### **URLs de Monitoramento**
- **Elasticsearch Health**: http://localhost:9200/_cluster/health
- **Logstash Stats**: http://localhost:9600/_node/stats
- **Kibana Status**: http://localhost:5601/api/status
- **Nginx Status**: http://localhost/nginx_status

### **Comandos Úteis**
```bash
# Ver logs de todos os serviços
docker-compose logs -f

# Ver logs específicos do Elasticsearch
docker-compose logs -f elasticsearch

# Verificar índices criados
curl http://localhost:9200/_cat/indices?v

# Estatísticas do cluster
curl http://localhost:9200/_cluster/stats?pretty
```

---

## 🧹 **Limpeza**

```bash
# Parar todos os serviços
docker-compose down

# Remover volumes (CUIDADO: apaga todos os dados)
docker-compose down -v

# Limpeza completa
docker system prune -a
```

---

## 📖 **Recursos Adicionais**

- [Documentação Oficial Elastic Stack](https://www.elastic.co/guide/index.html)
- [Nginx Log Format](https://nginx.org/en/docs/http/ngx_http_log_module.html)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Kibana Query Language (KQL)](https://www.elastic.co/guide/en/kibana/current/kuery-query.html)

---

## 🤝 **Contribuição**

Para sugestões e melhorias:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Abra um Pull Request

---

## 📝 **Changelog**

### **v2025.1**
- Migração para ELK Stack 8.11.3
- Adição de Filebeat e Metricbeat
- Logs estruturados em JSON
- Interface web interativa
- Health checks implementados
- Configurações otimizadas

---

**🎓 Desenvolvido para fins educacionais - Able2Cloud 2025** 