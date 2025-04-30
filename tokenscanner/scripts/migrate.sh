#!/bin/bash
set -euo pipefail

# This script is used to run the Alembic migrations for the database.

if [-z "${DATABASE_URL:-}"]; then
  echo "ERROR: DATABASE_URL is not set. Please set it before running this script."
  exit 1
fi

cd /app/src

alembic upgrade head
