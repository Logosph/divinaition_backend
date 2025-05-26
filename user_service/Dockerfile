FROM python:3.10
LABEL authors="logosph"

#WORKDIR /app
#COPY . .
#
#ENV PYTHONPATH=/app
#
#RUN apt-get update && \
#    pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH /app

RUN mkdir /app
WORKDIR /app

RUN apt-get update

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

