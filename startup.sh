#!/bin/sh

sleep 5

until pg_isready -h ${POSTGRES_HOST:-db} -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-postgres}; do
  echo "Waiting for db..."
  sleep 1
done

alembic upgrade head
