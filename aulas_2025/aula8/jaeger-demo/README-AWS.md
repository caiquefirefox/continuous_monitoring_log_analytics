# 🔍 Jaeger Demo - AWS Academy

## ⚠️ Para AWS Academy usar este arquivo!

### 1. Iniciar (AWS Academy)
```bash
docker-compose -f docker-compose-aws.yml up -d
```

### 2. Verificar se rodou
```bash
docker ps
```

### 3. Descobrir IP público da instância
```bash
curl -s http://169.254.169.254/latest/meta-data/public-ipv4
```

### 4. Acessar interfaces (substitua IP_PUBLICO)
- **Jaeger UI**: http://IP_PUBLICO:16686
- **HotROD**: http://IP_PUBLICO:8080

**Exemplo:** Se IP público for `54.123.45.67`:
- Jaeger: http://54.123.45.67:16686  
- HotROD: http://54.123.45.67:8080

### 5. Gerar traces
- Abra HotROD no navegador
- Clique em "Request a Ride" 
- Volte ao Jaeger UI e veja os traces

### 6. Parar
```bash
docker-compose -f docker-compose-aws.yml down
```

## ⚠️ **IMPORTANTE: Security Group**

As portas **16686** e **8080** precisam estar **liberadas** no Security Group!

### Liberar portas (AWS Academy):
1. Acesse EC2 → Security Groups
2. Selecione o Security Group da instância  
3. Editar Inbound Rules
4. Adicionar regras:
   - **Porta 16686** (Jaeger UI): TCP, Source: 0.0.0.0/0
   - **Porta 8080** (HotROD): TCP, Source: 0.0.0.0/0

## 🆘 Se não funcionar:

### Verificar portas:
```bash
netstat -tulpn | grep -E "(16686|8080|14268|6831)"
```

### Ver logs:
```bash
docker logs jaeger-aws
docker logs hotrod-aws
```

### Resetar:
```bash
docker-compose -f docker-compose-aws.yml down
docker system prune -f
docker-compose -f docker-compose-aws.yml up -d
```

## 🚀 **Script Automático**

Para facilitar, use o script que descobre o IP automaticamente:

```bash
chmod +x verificar-ip.sh
./verificar-ip.sh
```

Este script mostra os URLs corretos para copiar e colar no navegador!

---
**✨ Versão específica para AWS Academy** 