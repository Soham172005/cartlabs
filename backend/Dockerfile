FROM python:3.12-slim

ARG SERVICE_DIR
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/common:/app/service

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY common ./common
COPY ${SERVICE_DIR} ./service
WORKDIR /app/service

EXPOSE 8000
CMD python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000
