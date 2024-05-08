from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.base import BaseSensorOperator
from airflow.utils.decorators import apply_defaults
from datetime import datetime
import timeit
import time


class MyCustomSensor(BaseSensorOperator):
    @apply_defaults
    def __init__(self, xcom_to_pull, task_to_pull, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xcom_to_pull = xcom_to_pull
        self.task_to_pull = task_to_pull
    
    def poke(self, context):
        print(f"Poking at time interval : {timeit.default_timer()}")
        flag = False
        xcom_value = context["ti"].xcom_pull(key=self.xcom_to_pull, task_ids=self.task_to_pull)
        
        if xcom_value == "complete - success":
            print(f"Time of sensor True for {self.xcom_to_pull} : {timeit.default_timer()}")
            flag = True
        elif xcom_value == "complete - fail":
            print(f"Time of sensor error : {timeit.default_timer()}")
            raise AirflowException("Error encounter here. It should not pass")
        return flag

default_args = {
    "Owner" : "Subu",
    "start_date": datetime(2024, 4, 28),
    "retires": 1
}

dag = DAG(
    dag_id = "my_sensor_error_dag",
    default_args = default_args,
    schedule = None
)

def aggregates(**context):
    """
    Aggregates job mock
    """
    print(f"Starting the job ... at {timeit.default_timer()}")

    for i in range(5):
        print(f"Running for {i}th attempt ...")
        if i==3:
            context["ti"].xcom_push(key="weekly_aggs", value="complete - fail")
        
        print("sleeping for 10 seconds ...")
        time.sleep(10)
        print("sleep complete")


def insights(agg_type):
    print("Generating Insights ...")
    print(f"{agg_type} insights generated")
    print(f"Insights generated at time for {agg_type} : {timeit.default_timer()}")



aggregates_task = PythonOperator(
    task_id = "aggregates_task",
    dag = dag,
    python_callable = aggregates,
    provide_context = True
)

weekly_sensor = MyCustomSensor(
    task_id = "weekly_sensor",
    dag = dag,
    xcom_to_pull = "weekly_aggs",
    task_to_pull = "aggregates_task",
    mode = "poke",
    poke_interval = 1
)

weekly_insights = PythonOperator(
    task_id = "weekly_insights",
    dag = dag,
    python_callable = insights,
    op_kwargs = {"agg_type": "weekly"}
)

weekly_insights.set_upstream(weekly_sensor)


