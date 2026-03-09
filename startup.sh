#!/bin/sh

set -e

sleep 3

for i in $(seq 1 10); do
    if pg_isready -h "${POSTGRES_HOST:-db}" -U "${POSTGRES_USER:-postgres}" -d "${POSTGRES_DB:-postgres}" 2>/dev/null; then
        break
    fi
    echo "Waiting for db..."
    sleep 1
done

alembic upgrade head

cd /app
python -m pytest tests -v || (
    echo "Tests failed, stopping container"
    exit 1
)

echo "All checks passed, starting server..."
uvicorn src.main:app --host 0.0.0.0 --port 8000
