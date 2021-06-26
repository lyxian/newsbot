from airflow.providers.sqlite.operators.sqlite import SqliteOperator, CustomSqliteOperator
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import date, datetime, timedelta

default_args = {
    'owner': 'Lyx',
    'depends_on_past': False,
    'start_date': datetime(2021, 6, 21),
    # 'concurrency': 1,
    'email': ['lyxlyxi@hotmail.com'],
    'email_on_failure': False,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    dag_id='sqlite_dag',
    default_args=default_args,
    schedule_interval='0 7 * * *',
    # catchup=False
)

t1 = CustomSqliteOperator(
    task_id='select_query',
    sqlite_conn_id='conn_1',
    # sql='/scripts/create_table.sql',
    # sql='SELECT * FROM sqlite_master WHERE type = "table"',
    sql='SELECT chat_id, username FROM user',
    dag=dag,
)

def testing(ti):
    records = ti.xcom_pull(key='return_value', task_ids=['select_query'])
    print(records)

t2 = PythonOperator(
    task_id='step_2',
    python_callable=testing,
    dag=dag,
)

t1 >> t2