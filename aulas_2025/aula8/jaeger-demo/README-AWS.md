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

### 3. Acessar interfaces
- **Jaeger UI**: http://localhost:16686
- **HotROD**: http://localhost:8080

### 4. Gerar traces
- Abra HotROD no navegador
- Clique em "Request a Ride" 
- Volte ao Jaeger UI e veja os traces

### 5. Parar
```bash
docker-compose -f docker-compose-aws.yml down
```

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

---
**✨ Versão específica para AWS Academy** 