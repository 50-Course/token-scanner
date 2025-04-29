!/usr/bin/env bash
set -euo pipefail

# we should find a way to load our environment variables first
# (if file is present)
if [ -f /app/src/.env ]; then
  export $(cat /app/src/.env | xargs)
fi

exec uvicorn src.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload
