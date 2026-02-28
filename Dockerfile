FROM python:3.12-slim

# Evita prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Diretório da app
WORKDIR /app

# Instala dependências do sistema (PostgreSQL client e build tools)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação
COPY . .

# Copia scripts de CICD
COPY CICD/*.sh /app/CICD/
RUN chmod +x /app/CICD/*.sh

# Expõe porta padrão do Django
EXPOSE 8000