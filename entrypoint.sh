#!/usr/bin/env sh
set -eu

# Wait for Postgres using psycopg2 so we don't need extra OS packages
python - <<'PY'
import os, time
import psycopg2
host = os.environ.get('POSTGRES_HOST', 'db')
port = int(os.environ.get('POSTGRES_PORT', '5432'))
user = os.environ.get('POSTGRES_USER', 'postgres')
password = os.environ.get('POSTGRES_PASSWORD', '')
db = os.environ.get('POSTGRES_DB', 'multitenant')
while True:
    try:
        psycopg2.connect(host=host, port=port, user=user, password=password, dbname=db).close()
        break
    except Exception as e:
        print(f"Waiting for Postgres at {host}:{port} ... {e}")
        time.sleep(1)
print("Postgres is ready")
PY

# Create migrations if not present (idempotent)
python manage.py makemigrations tenancy patients --noinput || true

# Run migrations for public and tenants
python manage.py migrate_schemas --shared --noinput

# Start the server (gunicorn)
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3
