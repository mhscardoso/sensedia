#!/bin/sh

set -e

echo "Aplicando Migrations..."
python manage.py migrate

exec "$@"
