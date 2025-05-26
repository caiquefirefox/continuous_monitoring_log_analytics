# Laboratório Atualizado: Jaeger para Rastreamento Distribuído com Docker Compose - AWS Academy

Este guia demonstra como configurar e utilizar o Jaeger para rastreamento distribuído (distributed tracing) usando Docker Compose no ambiente AWS Academy. Ele abrange:
- Configuração de um ambiente com Docker Compose
- Implementação de uma aplicação Python simples que envia spans para o Jaeger
- Visualização e análise de traces na interface gráfica do Jaeger via IP público da EC2

✅ **Data da Atualização: 21 de Maio de 2025**

---

## 1. Estrutura do Projeto

```
jaeger-demo/
├── app.py                # Aplicação Python que envia spans para o Jaeger
├── Dockerfile            # Definição da imagem Docker para a aplicação Python
├── docker-compose.yml    # Configuração do Docker Compose com Jaeger e a aplicação
└── requirements.txt      # Dependências Python necessárias
```

---

## 2. Configuração do Ambiente

### 2.1. Obter o Código-fonte
```bash
# Execute na instância EC2 da AWS Academy
git clone https://github.com/able2cloud/continuous_monitoring_log_analytics.git
cd continuous_monitoring_log_analytics/aulas_2025/aula7/jaeger-demo

# Verificar se todos os arquivos estão presentes
ls -la
# Deve mostrar: app.py, Dockerfile, docker-compose.yml, requirements.txt
```

### 2.2. Verificar Pré-requisitos
```bash
# Verificar se o Docker está instalado e funcionando (execute na instância EC2 da AWS Academy)
sudo systemctl status docker

# Se necessário, instalar o Docker (apenas se não estiver instalado)
sudo apt-get update
sudo apt-get install docker.io docker-compose-plugin -y
sudo usermod -aG docker $USER
newgrp docker
```

---

## 3. Arquivos do Projeto

### 3.1. app.py - Aplicação Python
```python
import time
import opentracing
from jaeger_client import Config

def init_jaeger_tracer(service_name='my_service'):
    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'logging': True,
        },
        service_name=service_name,
        validate=True,
    )
    return config.initialize_tracer()

if __name__ == "__main__":
    tracer = init_jaeger_tracer()
    with tracer.start_span('test_span') as span:
        span.set_tag('example_tag', 'test_value')
        span.log_kv({'event': 'test_message', 'life': 42})
        time.sleep(1)
    tracer.close()
```

### 3.2. requirements.txt - Dependências Python
```
opentracing
jaeger-client
```

### 3.3. Dockerfile - Definição da Imagem Docker
```dockerfile
# Use uma imagem base oficial do Python
FROM python:3.12

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos da aplicação
COPY . .

# Comando para executar a aplicação
CMD ["python", "app.py"]
```

### 3.4. docker-compose.yml - Configuração dos Serviços
```yaml
version: '3'

services:
  jaeger:
    image: jaegertracing/all-in-one:1.29
    ports:
      - "5775:5775/udp"
      - "6831:6831/udp"
      - "6832:6832/udp"
      - "5778:5778"
      - "16686:16686"
      - "14268:14268"
      - "14250:14250"
      - "9411:9411"
    environment:
      - COLLECTOR_ZIPKIN_HTTP_PORT=9411

  python-app:
    build: .
    environment:
      - JAEGER_AGENT_HOST=jaeger
    depends_on:
      - jaeger
```

---

## 4. Executando a Demo

### 4.1. Construir e Iniciar os Contêineres
```bash
# Construir e iniciar os contêineres (execute na instância EC2 da AWS Academy)
sudo docker compose up --build

# O comando acima irá:
# 1. Construir a imagem da aplicação Python
# 2. Baixar a imagem do Jaeger
# 3. Iniciar ambos os serviços
# 4. A aplicação Python executará uma vez e enviará um trace para o Jaeger

# Aguarde até ver mensagens como:
# "python-app-1 exited with code 0" (aplicação terminou com sucesso)
# "jaeger-1 | ... Jaeger server started"
```

### 4.2. Verificar se os Serviços Estão Rodando
```bash
# Verificar se os contêineres estão rodando (execute na instância EC2 da AWS Academy)
sudo docker compose ps

# Deve mostrar:
# - jaeger: rodando (Up)
# - python-app: pode mostrar "Exited (0)" pois executa apenas uma vez

# Verificar logs do Jaeger
sudo docker compose logs jaeger

# Verificar logs da aplicação Python
sudo docker compose logs python-app
```

---

## 5. Acessar a Interface do Jaeger

### 5.1. Configurar Acesso via IP Público
**No ambiente AWS Academy, acesse via navegador:**
```
http://<IP_PUBLICO_DA_EC2>:16686
```

**Onde:**
- `<IP_PUBLICO_DA_EC2>` deve ser substituído pelo endereço IP público da sua instância EC2 da AWS Academy
- A porta `16686` é a porta padrão da interface web do Jaeger

**Para encontrar o IP público da sua instância EC2:**
1. Acesse o console da AWS Academy
2. Vá para EC2 > Instances
3. Localize sua instância e copie o "Public IPv4 address"

**Importante:** Certifique-se de que o Security Group da instância EC2 permite tráfego de entrada na porta 16686.

### 5.2. Verificar Conectividade Local
```bash
# Teste local para verificar se o Jaeger está respondendo (execute na instância EC2 da AWS Academy)
curl -I http://localhost:16686

# Deve retornar algo como "HTTP/1.1 200 OK"
```

---

## 6. Visualização dos Traces

### 6.1. Passos para Visualizar os Traces
1. Acesse `http://<IP_PUBLICO_DA_EC2>:16686` no seu navegador
2. A interface do Jaeger será carregada
3. No campo **"Service"** (canto superior esquerdo), selecione `my_service` (nome do serviço definido no script Python)
4. Clique no botão **"Find Traces"** (Encontrar Traces)
5. Uma lista de traces será exibida. Clique em qualquer trace para visualizar detalhes, incluindo:
   - **Spans**: Segmentos de operação
   - **Tags**: Metadados associados (`example_tag: test_value`)
   - **Logs**: Eventos registrados (`test_message`, `life: 42`)
   - **Tempo de execução**: Duração de cada span

### 6.2. Interpretando os Dados
Na interface do Jaeger, você verá:

- **Timeline**: Linha do tempo mostrando quando cada span ocorreu
- **Span Details**: Informações detalhadas sobre cada operação
- **Service Map**: Mapa visual dos serviços (se houver múltiplos serviços)
- **Dependencies**: Dependências entre serviços

### 6.3. Explorar Funcionalidades
1. **Filtros**: Use filtros de tempo, operação, tags para buscar traces específicos
2. **Comparison**: Compare traces diferentes para análise de performance
3. **JSON View**: Visualize os dados brutos do trace
4. **Graph View**: Visualização gráfica das relações entre spans

---

## 7. Executar Múltiplas Traces

### 7.1. Gerar Mais Traces para Análise
```bash
# Para gerar mais traces, execute novamente a aplicação Python (execute na instância EC2 da AWS Academy)
sudo docker compose run --rm python-app

# Repita o comando algumas vezes para gerar múltiplos traces
sudo docker compose run --rm python-app
sudo docker compose run --rm python-app
sudo docker compose run --rm python-app
```

### 7.2. Modificar a Aplicação (Opcional)
Para um exemplo mais interessante, você pode modificar o `app.py`:

```python
import time
import random
import opentracing
from jaeger_client import Config

def init_jaeger_tracer(service_name='my_service'):
    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'logging': True,
        },
        service_name=service_name,
        validate=True,
    )
    return config.initialize_tracer()

def process_data():
    """Simula processamento de dados"""
    time.sleep(random.uniform(0.1, 0.5))
    return "processed_data"

def save_to_database():
    """Simula salvamento no banco de dados"""
    time.sleep(random.uniform(0.2, 0.8))
    return "saved"

if __name__ == "__main__":
    tracer = init_jaeger_tracer()
    
    with tracer.start_span('main_operation') as main_span:
        main_span.set_tag('operation_type', 'data_processing')
        
        # Span filho para processamento
        with tracer.start_span('process_data', child_of=main_span) as process_span:
            process_span.set_tag('input_size', random.randint(100, 1000))
            result = process_data()
            process_span.log_kv({'event': 'data_processed', 'result': result})
        
        # Span filho para salvamento
        with tracer.start_span('save_data', child_of=main_span) as save_span:
            save_span.set_tag('database', 'postgresql')
            status = save_to_database()
            save_span.log_kv({'event': 'data_saved', 'status': status})
        
        main_span.log_kv({'event': 'operation_completed', 'total_items': 1})
    
    tracer.close()
```

Se modificar o arquivo, reconstrua e execute:
```bash
# Reconstruir e executar com o código modificado
sudo docker compose up --build python-app
```

---

## 8. Troubleshooting

### 8.1. Verificações Básicas
```bash
# Verificar se todos os contêineres estão rodando
sudo docker compose ps

# Verificar logs do Jaeger para erros
sudo docker compose logs jaeger | tail -20

# Verificar logs da aplicação Python
sudo docker compose logs python-app

# Verificar conectividade de rede
sudo docker compose exec jaeger curl -I http://localhost:16686
```

### 8.2. Problemas Comuns

**Jaeger não acessível via IP público:**
- Verifique se o Security Group permite tráfego na porta 16686
- Teste localmente primeiro: `curl http://localhost:16686`
- Confirme que o IP público da EC2 está correto

**Nenhum trace aparece na interface:**
```bash
# Verificar se a aplicação Python está enviando dados
sudo docker compose logs python-app | grep -i jaeger

# Executar novamente a aplicação
sudo docker compose run --rm python-app

# Verificar se o Jaeger está recebendo dados
sudo docker compose logs jaeger | grep -i span
```

**Erro de build da aplicação Python:**
```bash
# Verificar se todos os arquivos estão presentes
ls -la

# Limpar imagens e reconstruir
sudo docker compose down
sudo docker system prune -f
sudo docker compose up --build
```

---

## 9. Limpeza dos Recursos

### 9.1. Parar os Serviços
```bash
# Parar todos os contêineres (execute na instância EC2 da AWS Academy)
sudo docker compose down

# Para remover também os volumes (se houver)
sudo docker compose down -v
```

### 9.2. Limpeza Completa
```bash
# Remover imagens criadas (opcional)
sudo docker image prune -f

# Remover contêineres parados
sudo docker container prune -f

# Voltar ao diretório anterior
cd ../../../..
```

---

## 10. Considerações para AWS Academy

### 10.1. Security Groups
Certifique-se de que o Security Group da instância EC2 permite:
- **Porta 16686** (HTTP) para a interface web do Jaeger

### 10.2. Monitoramento de Recursos
- O Jaeger pode consumir recursos significativos de CPU e memória
- Monitore o uso de recursos da instância EC2
- Sempre pare os contêineres quando não estiver usando

### 10.3. Extensões Possíveis
Para laboratórios mais avançados, você pode:
- Integrar com outras aplicações microserviços
- Configurar sampling rules personalizadas
- Implementar OpenTelemetry
- Conectar com sistemas de alertas

---

## 11. Próximos Passos

### 11.1. Exploração Adicional
1. **Documentação do Jaeger**: https://www.jaegertracing.io/docs/
2. **OpenTracing**: https://opentracing.io/
3. **Instrumentação avançada**: Explore bibliotecas para frameworks web (Flask, Django, FastAPI)

### 11.2. Integração com Kubernetes
Para ambientes mais complexos, considere:
- Deployment do Jaeger no Kubernetes
- Sidecar pattern com Jaeger agent
- Integração com Prometheus e Grafana

#### 11.2.1. Exposição de Serviços Jaeger no Kubernetes
Se você instalar o Jaeger no Kubernetes (via Helm ou Operator), frequentemente o serviço será criado como ClusterIP. Para expô-lo no ambiente AWS Academy, use:

```bash
# Exemplo: Converter serviço Jaeger de ClusterIP para NodePort
sudo kubectl patch svc jaeger-query \
  -p '{
    "spec": {
      "type": "NodePort",
      "ports": [
        {
          "name": "http-query",
          "port": 16686,
          "targetPort": 16686,
          "nodePort": 31686,
          "protocol": "TCP"
        }
      ]
    }
  }'

# Verificar a mudança
sudo kubectl get svc jaeger-query
```

**Por que isso é útil:**
- Jaeger Operator e Helm charts geralmente criam serviços ClusterIP
- Permite acesso via IP público da EC2 sem recriar recursos
- Essencial para visualizar traces no ambiente AWS Academy

---

Com isso, você tem um ambiente completo de distributed tracing funcionando no AWS Academy, acessível via IP público da EC2, com traces visualizáveis na interface web do Jaeger para análise de performance e debugging de aplicações distribuídas. 