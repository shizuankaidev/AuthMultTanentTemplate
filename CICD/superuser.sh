#!/bin/bash
# superuser.sh - cria superuser Django a partir de variáveis de ambiente

: "${SUPERUSER:=false}"
: "${DJANGO_SUPERUSER_USERNAME:=admin}"
: "${DJANGO_SUPERUSER_EMAIL:=admin@email.com}"
: "${DJANGO_SUPERUSER_PASSWORD:=admin123}"

if [ "$SUPERUSER" = "true" ]; then
    echo "Verificando se superuser $DJANGO_SUPERUSER_USERNAME existe..."

    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').first()

if not user:
    user = User.objects.create_superuser(
        username='$DJANGO_SUPERUSER_USERNAME',
        email='$DJANGO_SUPERUSER_EMAIL',
        password='$DJANGO_SUPERUSER_PASSWORD',
        user_type='ADMIN'
    )
    print('Superuser criado com sucesso como ADMIN!')
else:
    updated = False

    if not user.is_superuser:
        user.is_superuser = True
        updated = True

    if not user.is_staff:
        user.is_staff = True
        updated = True

    if user.user_type != 'ADMIN':
        user.user_type = 'ADMIN'
        updated = True

    if updated:
        user.save()
        print('Usuário existente atualizado para superuser ADMIN.')
    else:
        print('Superuser já existe e já está configurado corretamente.')
"
else
    echo "SUPERUSER=false, pulando criação do superuser."
fi