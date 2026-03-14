#!/bin/bash
set -e

echo "Running database migrations..."
flask db upgrade

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 --pythonpath /app wsgi:app
