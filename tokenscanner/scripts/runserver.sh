#!/bin/bash
set -euo pipefail

# we should find a way to load our environment variables first
# (if file is present)
if [ -z "${DATABASE_URI:-}" ] && [ -f /app/src/.env ]; then
  export $(grep -v '^#' /app/src/.env | xargs -d '\n')
fi

# ensure DATABASE_URL is set
# if [ -z "${DATABASE_URI:-}" ]; then
#   echo "ERROR: DATABASE_URL is not set. Please set it before running this script."
#   exit 1
# fi

# we migrate
echo "[ENTRYPOINT]: Beginning database migrations..."
/app/scripts/migrate.sh

# finally, we run the server
echo "[ENTRYPOINT]: Starting FastAPI server..."
exec uvicorn src.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload
