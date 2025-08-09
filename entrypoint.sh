#!/bin/sh

# if ["$DATABASE" = "postgres"]
# then
#     echo "Waiting for postgres..."

#     while ! nc -z $SQL_HOST $SQL_PORT; do
#       sleep 0.1
#     done

#     echo "PostgreSQL is up and running!"
# fi

if [ "${DATABASE}" = "postgres" ]; then
  echo "Waiting for Postgres at ${SQL_HOST}:${SQL_PORT} ..."
  # Ensure nc is available
  if ! command -v nc >/dev/null 2>&1; then
    echo "Error: 'nc' (netcat) not found in the container. Install netcat-openbsd."
    exit 1
  fi

  # Wait until the port is open
  while ! nc -z "${SQL_HOST}" "${SQL_PORT}"; do
    sleep 0.1
  done
  echo "PostgreSQL is up!"
fi

# Apply database migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput

exec "$@"