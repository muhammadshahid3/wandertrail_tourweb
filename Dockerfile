FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py

WORKDIR /app

# PyMySQL and psycopg2-binary are pure wheels, so no apt build tools are needed.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/app/static/images/uploads

EXPOSE 5000

# --preload: create tables + seed admin ONCE in the master process,
# so the 3 workers do not race each other at startup.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--timeout", "120", "--preload", "run:app"]
