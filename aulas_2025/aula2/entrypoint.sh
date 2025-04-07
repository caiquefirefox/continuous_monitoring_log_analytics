#!/bin/sh

set -e

echo "[Zabbix] Aguardando MySQL estar pronto..."
until mysql -h mysql -uzabbix -pzabbix -e "SELECT 1;" > /dev/null 2>&1; do
  sleep 2
done

echo "[Zabbix] Verificando tabela 'users'..."
USERS_COUNT=$(mysql -h mysql -uzabbix -pzabbix -Nse "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'zabbix' AND table_name = 'users';")

if [ "$USERS_COUNT" -eq 0 ]; then
  echo "[Zabbix] Aplicando schema inicial no banco de dados..."
  zcat /usr/share/zabbix-sql-scripts/mysql/server.sql.gz | mysql -h mysql -uzabbix -pzabbix zabbix
else
  echo "[Zabbix] Banco de dados já possui schema. Prosseguindo..."
fi

echo "[Zabbix] Iniciando Zabbix Server..."
exec /usr/sbin/zabbix_server -c /etc/zabbix/zabbix_server.conf
