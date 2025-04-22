#!/usr/bin/env bash

# Wait for DB to be ready (optional, requires "wait-for-it" or similar)

# Apply database migrations
python manage.py migrate --noinput

# Optionally create superuser if needed

# Execute the specified command
exec "$@"