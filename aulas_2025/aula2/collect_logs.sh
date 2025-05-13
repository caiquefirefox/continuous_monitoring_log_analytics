#!/bin/bash

echo "============ ZABBIX SERVER LOGS ============"
docker logs aula2-zabbix-server-1 2>&1 | tail -30

echo ""
echo "============ ZABBIX WEB LOGS ============"
docker logs aula2-zabbix-web-1 2>&1 | tail -30

echo ""
echo "============ ZABBIX AGENT LOGS ============"
docker logs aula2-zabbix-agent-1 2>&1 | tail -30

echo ""
echo "============ ZABBIX DB LOGS ============"
docker logs aula2-zabbix-db-1 2>&1 | tail -30

echo ""
echo "============ CONTAINER STATUS ============"
docker ps -a

echo ""
echo "============ NETWORK INFO ============"
docker network inspect bridge 