FROM python:3.10
LABEL authors="logosph"

ENV PYTHONPATH /app

RUN mkdir /app
WORKDIR /app

RUN apt-get update

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

