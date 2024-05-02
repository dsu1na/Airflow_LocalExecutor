FROM python:3.11-slim

RUN mkdir /airflow

ENV AIRFLOW_HOME=/airflow
COPY requirements.txt .
COPY airflow_setup_files/airflow_postgres_db.sh .
COPY airflow_setup_files/setup_airflow.sh .
COPY dags/xcom_spending_natwest.py /airflow/dags

RUN apt-get update \
    && apt-get install sudo \
    && sudo apt-get install -y gcc python3-dev \
    && apt install -y git \
    && sudo apt-get install -y postgresql postgresql-contrib \
    && pip3 install --no-cache-dir -r requirements.txt

# To start postgres server / process RUN 
# sudo service postgresql start

# To enter the postgres terminal cmd line RUN
# sudo -u postgres psql

# Edit the airflow.cfg file 
# edit executor to LocalExecutor, edit sqlAlchemy to postgresql+psycopg2://airflow:airflow@localhost/airflow