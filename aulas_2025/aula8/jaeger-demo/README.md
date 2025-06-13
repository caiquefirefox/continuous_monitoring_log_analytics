# 🔍 Jaeger Tracing Demo 2025

## Melhorias Implementadas

### ✨ **Principais Atualizações**
- **Jaeger 1.54** (vs 1.48 anterior)
- **OpenTelemetry** ao invés de bibliotecas legacy
- **Python 3.12** com multi-stage Docker build
- **HotROD app** para demonstrações avançadas
- **Health checks** em todos os serviços
- **Prometheus + Grafana** para métricas
- **Load generator** automático

### 🚀 **Como Usar**

```bash
# Iniciar todos os serviços
docker-compose up -d

# Ver logs da aplicação Python
docker-compose logs -f python-app

# Parar tudo
docker-compose down
```

### 🌐 **Interfaces**
- **Jaeger UI**: http://localhost:16686
- **HotROD App**: http://localhost:8080
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin123)

### 🎯 **O que mudou?**

#### **1. Aplicação Python**
- Migrou de `jaeger-client` para `opentelemetry-*`
- Simula jornada completa do usuário (auth → order → payment → notification)
- Spans mais complexos com atributos e eventos
- Instrumentação automática de requests

#### **2. Arquitetura**
- Volumes persistentes para dados
- Network dedicada
- Health checks nativos
- Restart policies configuradas

#### **3. Monitoramento**
- HotROD para simulação de microserviços
- Prometheus para métricas
- Grafana para visualização
- Load generator automático

### 📊 **Traces Gerados**
A aplicação Python gera traces realistas simulando:
- Autenticação OAuth2
- Processamento de pedidos
- Validação de estoque
- Cálculo de frete
- Gateway de pagamento
- Notificações multi-canal

Cada trace inclui latências realistas, falhas ocasionais e atributos detalhados para análise.

---

**✨ Versão 2025 - Modernizada com OpenTelemetry e melhores práticas** 