#!/bin/bash
set -euo pipefail


# This script is used to run the Alembic migrations for the database.

# if [ -z "${DATABASE_URI:-}" ]; then
#   echo "ERROR: DATABASE_URL is not set. Please set it before running this script."
#   exit 1
# fi

alembic -c /app/alembic.ini upgrade head
# alembic revision --autogenerate -m "Initial migration"
