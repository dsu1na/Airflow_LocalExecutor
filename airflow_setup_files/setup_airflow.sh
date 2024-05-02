airflow db migrate
airflow users create --username admin --password password --firstname Toni --lastname Kutta --role Admin --email tonikutta@gmail.com
airflow webserver -p 8080 --daemon
airflow scheduler --daemon