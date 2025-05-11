#!/bin/bash
set -euo pipefail

# This script is used to run the Alembic migrations for the database.

# if [ -z "${DATABASE_URI:-}" ]; then
#   echo "ERROR: DATABASE_URL is not set. Please set it before running this script."
#   exit 1
# fi

echo "[ALEMBIC|ENTRYPOINT]: Running initial migrations..."
alembic revision --autogenerate -m "Initial migration"
echo "[ALEMBIC|ENTRYPOINT]: Applying database migrations..."
alembic upgrade head
echo "[ALEMBIC|ENTRYPOINT]: Database migrations completed..."
# alembic -c /app/alembic.ini upgrade head
