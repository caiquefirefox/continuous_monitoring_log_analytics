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
