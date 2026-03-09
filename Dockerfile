FROM python:3.12-slim

WORKDIR /app

# Cached pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app/src

# Tests in container
COPY ./tests /app/tests

# Alembic
COPY alembic.ini .
COPY ./alembic /app/alembic
COPY ./startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh

# Starting
CMD ["/app/startup.sh"]
