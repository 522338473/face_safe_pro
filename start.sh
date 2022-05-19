#!/bin/bash

#pipenv run python manage.py migrate
#pipenv run python manage.py runserver 0.0.0.0:8000


if [ $1 ]; then
  if [ $1 = 'celery' ]; then
    pipenv run python manage.py makemigrations
    pipenv run python manage.py migrate
    pipenv run celery -A face_safe worker -B -l info
  else
    pipenv run python manage.py makemigrations
    pipenv run python manage.py migrate
    pipenv run python manage.py $1
  fi
else
  echo "default"
  pipenv run python manage.py makemigrations
  pipenv run python manage.py migrate
  export DJANGO_SUPERUSER_PASSWORD=Yishi@9086
  pipenv run python manage.py createsuperuser --noinput --username Yishi  --email Yishi@localhost.com
  pipenv run daphne -b 0.0.0.0 -p 9999 face_safe_pro.asgi:application
fi
