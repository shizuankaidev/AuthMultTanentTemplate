# 🚀 Template Pronto e Seguro - By Shizu Dev

## 🔹 Requisitos

- Python  3.13  (python --version)
- Docker  
- PostgreSQL  

---

## 🔹 Configuração do `.env`

Crie um arquivo `.env` com as seguintes variáveis:

para iniciar corretamente, a primeira inicialização tem que ter

SUPERUSER       =true
MIGRATION       =true
RESETDATABASE   =true


```dotenv

    DEBUG=True

    SECRET_KEY=django-insecure-7xK9vQ!Shizu_4mTz#pL2r@8NwE6yU$1cHfR3bA
    ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0

    DB_NAME=crm_db
    DB_USER=crm_user
    DB_PASSWORD=crm_pass
    DB_HOST=db
    DB_PORT=5432


    SUPERUSER=true
    DJANGO_SUPERUSER_USERNAME=admin
    DJANGO_SUPERUSER_EMAIL=admin@email.com
    DJANGO_SUPERUSER_PASSWORD=admin

    MIGRATION=true
    RESETDATABASE=true

```

## 🔹 Inicialização do Projeto

Siga os passos abaixo para iniciar o projeto com Docker:

### 1. **Criar e ativar o ambiente virtual Python**  

```bash
# Windows
py -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

#### Instalar dependências do Python

```
pip install -r requirements.txt
```
#### Inicializar o Docker e subir os containers

```
docker compose up --build
```
⚡ Isso irá construir os containers e inicializar a aplicação automaticamente, pronta para uso.
    Apos isso troque para:

SUPERUSER       =false
MIGRATION       =false
RESETDATABASE   =false

======================================================================================================

O objetivo deste projeto é resolver um problema que venho enfrentando há algum tempo: a criação repetitiva de uma estrutura com a qual já estou familiarizado. Sei que não sou um programador expert, mas sigo boas práticas de segurança. Com isso, espero que mais pessoas possam contribuir para este template, cujo foco é:

- Autenticação e login

- Segurança com JWT

- Controle de limite de acesso (Range Limit)

- Modelo com Multi-Tenant

Dessa forma, teremos um ponto de partida sólido para backends, permitindo que a partir deste template seja possível construir qualquer outra aplicação de forma segura e organizada.

