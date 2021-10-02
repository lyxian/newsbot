from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import date, datetime, timedelta

default_args = {
    'owner': 'Lyx',
    'depends_on_past': False,
    'start_date': datetime(2021, 8, 28),
    # 'concurrency': 1,
    'email': ['lyxlyxi@hotmail.com'],
    'email_on_failure': False,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

ts = "{{ ts }}"
ds = "{{ ds }}"

dag = DAG(
    dag_id='test_backfill',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=True,
)

temp_dict = {
    'ts': '{{ ts }}',
    'ds': '{{ ds }}'
}

def x(templates_dict):
    msg = f'''Timestamp: {templates_dict['ts']}
    Date: {templates_dict['ds']}'''
    print(msg)
    print()
    print(templates_dict)

t1 = PythonOperator(
    task_id='get_time',
    python_callable=x,
    templates_dict=temp_dict,
    dag=dag,
)

t1