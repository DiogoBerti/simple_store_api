#!/bin/sh
sleep 10
#python manage.py makemigrations
python manage.py migrate auth
python manage.py migrate --run-syncdb
python manage.py loaddata store_main/fixtures/users.json
pytest -s
python manage.py runserver 0.0.0.0:8000

