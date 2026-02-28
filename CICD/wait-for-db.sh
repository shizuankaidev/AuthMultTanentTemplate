#!/bin/bash
# entrypoint.sh - espera DB, aplica reset/migrations e inicia Django
set -e

host="$1"
shift

echo "Esperando o banco em $host..."
until pg_isready -h "$host" -U "$DB_USER"; do
  echo "Banco não disponível ainda, tentando de novo..."
  sleep 2
done
echo "Banco pronto!"

# Reset do banco se necessário
if [ "${RESETDATABASE:=false}" = "true" ]; then
    echo "RESETDATABASE=true, resetando banco ${DB_NAME}..."
    PGPASSWORD="$DB_PASSWORD" dropdb -h "$host" -U "$DB_USER" --if-exists "$DB_NAME"
    PGPASSWORD="$DB_PASSWORD" createdb -h "$host" -U "$DB_USER" "$DB_NAME"
    echo "Banco resetado com sucesso!"
fi

# Aplicar migrations se necessário
if [ "${MIGRATION:=false}" = "true" ]; then
    echo "MIGRATION=true, aplicando migrations..."
    python manage.py makemigrations
    python manage.py migrate
    echo "Migrations aplicadas!"
fi

# Criar superuser se habilitado
/app/CICD/superuser.sh

# Iniciar Django
exec "$@"