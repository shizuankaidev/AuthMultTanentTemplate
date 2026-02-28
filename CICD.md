docker compose build --no-cache 

docker compose up

-- aguarde --

docker compose run web python manage.py makemigrations
docker compose run web python manage.py migrate

