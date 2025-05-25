FROM python:3.10
LABEL authors="logosph"

WORKDIR /app
COPY . /app

ENV PYTHONPATH=/app

RUN apt-get update
RUN pip install --no-cache-dir -r requirements.txt
