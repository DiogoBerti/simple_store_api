#!/bin/sh
python manage.py makemigrations
python manage.py migrate auth
python manage.py migrate --run-syncdb
python manage.py runserver 0.0.0.0:8000

