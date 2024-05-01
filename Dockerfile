FROM python:3.11-slim

RUN mkdir /airflow

ENV AIRFLOW_HOME=/airflow
# COPY requirements.txt .

RUN apt-get update \
    && apt-get install sudo \
    && sudo apt-get install -y gcc python3-dev \
    && apt install -y git \
    && sudo apt-get install python-psycopg2 \
    && sudo apt-get install postgresql postgresql-contrib 
    # && pip3 install --no-cache-dir -r requirements.txt