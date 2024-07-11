#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Set default values for admin user
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"johndoe42@example.com"}

cd /app/

# Set Django settings module
export DJANGO_SETTINGS_MODULE=config.settings.local

# Ensure the static directory exists
mkdir -p /app/static

# Collect static files for the Django project
python manage.py collectstatic --noinput
>&2 echo 'Collected static files...'

# Run database migrations
/opt/venv/bin/python manage.py migrate --noinput || true
>&2 echo 'Ran database migrations...'

# Create the superuser
/opt/venv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true
>&2 echo 'Created superuser...'

# Set the application port, defaulting to 8000 if not set
APP_PORT=${PORT:-8000}

# Start the Gunicorn server to serve the Django application
>&2 echo 'About to run Gunicorn...'
/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm config.wsgi:application --bind "0.0.0.0:${APP_PORT}" --timeout 600

