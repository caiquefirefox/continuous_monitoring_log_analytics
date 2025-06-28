#!/bin/bash

echo "🔍 Descobrindo IP público da instância AWS..."
IP_PUBLICO=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

if [ -n "$IP_PUBLICO" ]; then
    echo "✅ IP público encontrado: $IP_PUBLICO"
    echo ""
    echo "🌐 URLs para acessar:"
    echo "   • Jaeger UI: http://$IP_PUBLICO:16686"
    echo "   • HotROD:    http://$IP_PUBLICO:8080"
    echo ""
    echo "📋 Para copiar e colar:"
    echo "http://$IP_PUBLICO:16686"
    echo "http://$IP_PUBLICO:8080"
else
    echo "❌ Não foi possível descobrir o IP público"
    echo "💡 Verifique manualmente no painel da AWS Academy"
fi 