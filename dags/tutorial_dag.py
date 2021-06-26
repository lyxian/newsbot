from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import date, datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'schedule_interval': '@hourly',
}

dag = DAG(
    dag_id='tutorial',
    default_args=default_args,
    catchup=False
)

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag
)