from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pendulum

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from TEST.utils.search import _searchArticles

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

temp_dict = {
    'curr': '{{ ts }}',
    'prev': '{{ prev_execution_date_success }}', #
    # 'e3': '{{ prev_execution_date }}', #
}

def searchArticles(templates_dict):
    curr_ts = pendulum.parse(templates_dict['curr']).in_tz(tz='Asia/Singapore')
    prev_ts = pendulum.parse(templates_dict['prev']).in_tz(tz='Asia/Singapore')
    new_articles = _searchArticles(curr_ts, prev_ts)
    print(f'Scanning articles from {prev_ts} -> {curr_ts}...')
    print(f'-------{len(new_articles)} new article(s)-------')
    print(new_articles)

    return

with DAG(
    dag_id='main_search',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False,
) as dag:
    search_articles = PythonOperator(
        task_id='search_articles',
        python_callable=searchArticles,
        templates_dict=temp_dict,
    )

search_articles