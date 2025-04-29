!/usr/bin/env bash
set -euo pipefail

# we should find a way to load our environment variables first
# (if file is present)
if [ -f /app/src/.env ]; then
  export $(cat /app/src/.env | xargs)
fi

# ensure DATABASE_URL is set
if [ -z "${DATABASE_URL:-}" ]; then
  echo "ERROR: DATABASE_URL is not set. Please set it before running this script."
  exit 1
fi

# we migrate
/app/src/migrate.sh

# finally, we run the server
exec uvicorn src.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload
