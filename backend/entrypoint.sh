#!/bin/sh

set -e 

echo "${0}: running migrations. :"
python manage.py makemigrations authentication
python manage.py makemigrations dashboaring
python manage.py migrate --noinput

echo "${0} : collect staticfile "
python manage.py collectstatic --noinput

# daphne -b 0.0.0.0 -p 8000 config.asgi:application 
gunicorn config.wsgi --bind 0.0.0.0:8000
