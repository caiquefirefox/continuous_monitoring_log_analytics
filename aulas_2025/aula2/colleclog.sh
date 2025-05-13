#!/usr/bin/env bash

# Define o arquivo de saída
LOGFILE="./logall.txt"

# Zera o conteúdo anterior (se existir)
: > "$LOGFILE"

# Lista dos nomes dos containers
CONTAINERS=(
  "aula2-zabbix-agent-1"
  "aula2-zabbix-db-1"
  "aula2-zabbix-web-1"
  "aula2-zabbix-server-1"
)

# Para cada container, stream os logs em background
for C in "${CONTAINERS[@]}"; do
  echo "Iniciando logs de $C → $LOGFILE"
  docker logs -f "$C" >> "$LOGFILE" 2>&1 &
done

# Aguarda todos os jobs terminarem (vai manter aberto enquanto os containers rodarem)
sleep 30; exit

