FROM python:3.10
LABEL authors="logosph"

WORKDIR /app
COPY . .

ENV PYTHONPATH=/app

RUN apt-get update && \
    pip install --no-cache-dir -r requirements.txt