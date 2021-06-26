from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import date, datetime, timedelta

default_args = {
    'owner': 'Lyx',
    'depends_on_past': False,
    'start_date': datetime(2021, 6, 22),
    # 'concurrency': 1,
    'email': ['lyxlyxi@hotmail.com'],
    'email_on_failure': False,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    dag_id='custom_bash_dag',
    default_args=default_args,
    schedule_interval='0 7 * * *',
    # catchup=False
)

t1 = BashOperator(
    task_id='bash_1',
    bash_command='py_ls -i ~/wSpace/Py',
    dag=dag,
)

t1