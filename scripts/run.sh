#!/bin/sh

# fail executinhg commands when one cmd fails
set -e

# collect static files and put them in a configured directory
python manage.py collectstatic --noinput

# apply migrations to database
python manage.py migrate


uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi



