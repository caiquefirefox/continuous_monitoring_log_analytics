# 🔍 Jaeger Demo - Lab Simples

## ⚡ Como usar

### 1. Iniciar
```bash
docker-compose -f docker-compose-simples.yml up -d
```

### 2. Abrir Jaeger UI
http://localhost:16686

### 3. Abrir HotROD
http://localhost:8080

### 4. Gerar traces
- Clique nos botões "Request a Ride" no HotROD
- Volte ao Jaeger UI e veja os traces

### 5. Parar
```bash
docker-compose -f docker-compose-simples.yml down
```

**Fim! 🎉** 