#!/usr/bin/env bash

set -e

chown www-data:www-data /var/log

while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
done

python manage.py migrate
python manage.py collectstatic --noinput

uwsgi --strict --ini /app/uwsgi.ini
