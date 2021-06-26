from airflow.providers.sqlite.operators.sqlite import CustomSqliteOperator
from airflow import DAG
from airflow.operators.python import PythonOperator, ShortCircuitOperator
from datetime import datetime, timedelta

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Py.DAG.main import searchArticles, sendToTelegram
import pendulum

default_args = {
    'owner': 'Lyx',
    'depends_on_past': False,
    'start_date': datetime(2021, 6, 25),       # == today - 1
    # 'concurrency': 1,
    'email': ['lyxlyxi@hotmail.com'],
    'email_on_failure': False,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='main',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False,
) as dag:
    check_hour = ShortCircuitOperator(
        task_id='skip_if_offline',
        python_callable=(lambda time: pendulum.parse(time).in_tz('Asia/Singapore').hour in [0, *range(9, 24)]),
        op_kwargs={
            'time': '{{ execution_date }}'
        }
    )
    search_articles = PythonOperator(
        task_id='search_articles',
        python_callable=searchArticles,
    )
    check_article = ShortCircuitOperator(
        task_id='skip_if_empty_article',
        python_callable=(lambda ti: ti.xcom_pull(key='new_articles', task_ids='search_articles')),
    )
    get_users = CustomSqliteOperator(
        task_id='select_query_user',
        sqlite_conn_id='conn_test',
        sql='SELECT chat_id, username FROM user',
    )
    check_user = ShortCircuitOperator(
        task_id='skip_if_empty_user',
        python_callable=(lambda ti: ti.xcom_pull(key='return_value', task_ids='select_query_user')),
    )
    send_to_telegram = PythonOperator(
        task_id='send_to_telegram',
        python_callable=sendToTelegram,
    )

check_hour >> search_articles >> check_article >> get_users >> check_user >> send_to_telegram