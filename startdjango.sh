#!/usr/bin/env bash

cd emarket

python manage.py makemigrations
python manage.py migrate --noinput

python loaddump.py

gunicorn emarket.wsgi:application --bind 0.0.0.0:8000
