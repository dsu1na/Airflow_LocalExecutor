# for starting the postgres server
sudo service postgresql start

# comands for airflow db setup
sudo -u postgres psql -c "CREATE USER airflow PASSWORD 'airflow';"
sudo -u postgres psql -c "CREATE DATABASE airflow;"
sudo -u postgres psql -d airflow -c "GRANT ALL ON SCHEMA public TO airflow;"