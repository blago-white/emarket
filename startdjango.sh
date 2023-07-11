#!/usr/bin/env bash

python emarket/manage.py migrate --noinput

python emarket/manage.py shell < "delete_content_types.py"

python emarket/manage.py loaddata dumped_data.json

python emarket/manage.py runserver 0.0.0.0:8000 --insecure
