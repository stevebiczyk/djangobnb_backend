#!/bin/sh

if ["$DATABASE" = "postgres"]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL is up and running!"
fi

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

exec "$@"