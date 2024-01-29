# Use uma imagem oficial do Python como base
FROM python:3.11

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos necessários para o contêiner
COPY requirements.txt .
COPY main.py .
COPY src/ ./src/
COPY data/ ./data/

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta necessária para o aplicativo Dash
EXPOSE 8050

# Comando para executar o aplicativo quando o contêiner for iniciado
CMD ["python", "main.py"]
