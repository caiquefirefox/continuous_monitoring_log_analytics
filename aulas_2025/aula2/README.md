# Guia do Lab – Alerta "Aula1" no Zabbix

## 📥 Clonando o repositório

```bash
git clone https://github.com/able2cloud/zabbix-lab-aula1.git
cd zabbix-lab-aula1
docker compose up -d
```

Acesse: [http://localhost:8080](http://localhost:8080)

**Login padrão:**
- Usuário: `Admin`
- Senha: `zabbix`

---

## 📌 Pré-requisitos
- Docker e Docker Compose instalados
- Ambiente iniciado com `docker compose up -d`

---

## 1. 🖥️ Criar um novo Host
1. No menu lateral, vá em **Configuration > Hosts**
2. Clique em **Create host**
3. Preencha:
   - **Host name:** `Aula1-App`
   - **Visible name:** `Aula1-App`
   - **Groups:** clique em `Select` e escolha `Linux servers`
   - **Agent interface:** `127.0.0.1` ou IP do container
4. Em **Templates > Add**, selecione:
   - `Template OS Linux by Zabbix agent`
5. Clique em **Add**

---

## 2. 📈 Criar um Item personalizado
1. Ainda no host `Aula1-App`, vá em **Items > Create item**
2. Preencha:
   - **Name:** `Carga da CPU Aula1`
   - **Type:** `Zabbix agent`
   - **Key:** `system.cpu.load[percpu,avg1]`
   - **Type of information:** `Numeric (float)`
   - **Update interval:** `30s`
3. Clique em **Add**

---

## 3. 🚨 Criar uma Trigger (regra de alerta)
1. Vá em **Triggers > Create trigger**
2. Preencha:
   - **Name:** `CPU alta no Aula1`
   - **Severity:** `High`
   - **Expression:** clique em **Add**
     - Escolha o item criado: `Carga da CPU Aula1`
     - Operador: `last() > 2`
     - Clique em **Insert**
3. Clique em **Add**

---

## 4. 🧪 Testar o alerta (gerar carga)

No container do agente Zabbix, execute:

```bash
docker exec -it aula2-zabbix-agent yes > /dev/null &
```

---

## 5. 👀 Ver o alerta ativo
1. Vá para **Monitoring > Problems**
2. Aguarde 1-2 minutos
3. Você verá o alerta “CPU alta no Aula1” com status `PROBLEM`

---

## 6. 🛑 Encerrar o teste

```bash
docker exec -it aula2-zabbix-agent killall yes
```

O alerta mudará para `RESOLVED`.
