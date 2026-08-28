import os
import sys
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv


# ============================================================
# CONFIGURAÇÃO
# ============================================================

# Diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega o .env da raiz
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# ============================================================
# VARIÁVEIS DO POSTGRESQL
# ============================================================

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")


# ============================================================
# VARIÁVEIS DO SUPABASE S3
# ============================================================

S3_ENDPOINT = os.getenv("SUPABASE_S3_ENDPOINT")
S3_REGION = os.getenv("SUPABASE_S3_REGION", "us-east-1")
S3_ACCESS_KEY = os.getenv("SUPABASE_S3_ACCESS_KEY_ID")
S3_SECRET_KEY = os.getenv("SUPABASE_S3_SECRET_ACCESS_KEY")
S3_BUCKET = os.getenv("SUPABASE_S3_BUCKET")


# ============================================================
# VALIDAÇÃO
# ============================================================

REQUIRED_ENV = {
    "DB_NAME": DB_NAME,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "SUPABASE_S3_ENDPOINT": S3_ENDPOINT,
    "SUPABASE_S3_ACCESS_KEY_ID": S3_ACCESS_KEY,
    "SUPABASE_S3_SECRET_ACCESS_KEY": S3_SECRET_KEY,
    "SUPABASE_S3_BUCKET": S3_BUCKET,
}


def validate_environment():
    missing = [
        key
        for key, value in REQUIRED_ENV.items()
        if not value
    ]

    if missing:
        print("ERRO: Variáveis de ambiente ausentes:")

        for key in missing:
            print(f"  - {key}")

        sys.exit(1)


# ============================================================
# ARGUMENTOS
# ============================================================

def get_store_id():
    if len(sys.argv) != 2:
        print(
            "Uso:\n"
            "  python backup/saveBackup.py <store_id>\n\n"
            "Exemplo:\n"
            "  python backup/saveBackup.py 1"
        )

        sys.exit(1)

    store_id = sys.argv[1]

    if not store_id.isdigit():
        print("ERRO: store_id deve ser um número inteiro.")

        sys.exit(1)

    return int(store_id)


# ============================================================
# CLIENTE S3
# ============================================================

def create_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        region_name=S3_REGION,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
    )


# ============================================================
# DELETAR BACKUPS ANTERIORES DA STORE
# ============================================================

def delete_old_backups(s3, store_id):
    prefix = f"stores/{store_id}/"

    print(
        f"Procurando backups antigos da Store {store_id}..."
    )

    try:
        response = s3.list_objects_v2(
            Bucket=S3_BUCKET,
            Prefix=prefix,
        )

    except ClientError as exc:
        print("ERRO ao listar backups antigos:")
        print(exc)

        sys.exit(1)

    objects = response.get("Contents", [])

    if not objects:
        print("Nenhum backup antigo encontrado.")
        return

    keys = [
        {"Key": obj["Key"]}
        for obj in objects
    ]

    print(
        f"Encontrados {len(keys)} backup(s) antigo(s)."
    )

    # S3 permite apagar vários objetos de uma vez.
    for i in range(0, len(keys), 1000):
        batch = keys[i:i + 1000]

        try:
            s3.delete_objects(
                Bucket=S3_BUCKET,
                Delete={
                    "Objects": batch,
                    "Quiet": True,
                },
            )

        except ClientError as exc:
            print("ERRO ao deletar backups antigos:")
            print(exc)

            sys.exit(1)

    print("Backups antigos removidos.")


# ============================================================
# PG_DUMP
# ============================================================

def create_database_dump(output_file):
    print("Criando backup do PostgreSQL...")

    env = os.environ.copy()

    # Evita pedir senha interativamente.
    env["PGPASSWORD"] = DB_PASSWORD

    command = [
        "pg_dump",
        "--host", DB_HOST,
        "--port", DB_PORT,
        "--username", DB_USER,
        "--dbname", DB_NAME,
        "--format=custom",
        "--file", str(output_file),
    ]

    try:
        subprocess.run(
            command,
            env=env,
            check=True,
        )

    except FileNotFoundError:
        print(
            "ERRO: pg_dump não foi encontrado."
        )

        sys.exit(1)

    except subprocess.CalledProcessError as exc:
        print(
            f"ERRO: pg_dump falhou com código {exc.returncode}."
        )

        sys.exit(1)

    print("Backup do PostgreSQL criado.")


# ============================================================
# UPLOAD
# ============================================================

def upload_backup(s3, store_id, backup_file):
    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%d_%H%M%S"
    )

    key = (
        f"stores/{store_id}/"
        f"backup_{timestamp}.dump"
    )

    print(
        f"Enviando backup para Supabase: {key}"
    )

    try:
        s3.upload_file(
            str(backup_file),
            S3_BUCKET,
            key,
        )

    except ClientError as exc:
        print("ERRO ao enviar backup:")
        print(exc)

        sys.exit(1)

    print("Backup enviado com sucesso.")

    return key


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("BACKUP DA STORE")
    print("=" * 60)

    validate_environment()

    store_id = get_store_id()

    print(f"Store selecionada: {store_id}")
    print(f"Bucket: {S3_BUCKET}")

    s3 = create_s3_client()

    # --------------------------------------------------------
    # Arquivo temporário
    # --------------------------------------------------------

    with tempfile.TemporaryDirectory() as temp_dir:

        backup_file = (
            Path(temp_dir)
            / f"store_{store_id}.dump"
        )

        # ----------------------------------------------------
        # 1. Criar dump
        # ----------------------------------------------------

        create_database_dump(
            backup_file
        )

        # ----------------------------------------------------
        # 2. Deletar backups antigos
        # ----------------------------------------------------

        delete_old_backups(
            s3,
            store_id
        )

        # ----------------------------------------------------
        # 3. Enviar novo backup
        # ----------------------------------------------------

        upload_backup(
            s3,
            store_id,
            backup_file
        )

    print("=" * 60)
    print("BACKUP FINALIZADO COM SUCESSO")
    print("=" * 60)


if __name__ == "__main__":
    main()