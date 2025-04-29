# This script is used to run the Alembic migrations for the database.
!/usr/bin/env bash
set -euo pipefail

if [-z "${DATABASE_URL:-}"]; then
  echo "ERROR: DATABASE_URL is not set. Please set it before running this script."
  exit 1
fi

cd /app/src

alembic upgrade head
