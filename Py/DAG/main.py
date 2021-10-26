# This module contains all helper functions for PythonOperator
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Database.models import Article, ArticleSchema, User, UserSchema, db
from Telegram.main import getToken
from utils.SQLite.query import sql_query, sql_table_columns
from utils.REST.helpers import _searchArticles

import pendulum
import requests
import logging

def searchArticles(ti, templates_dict):
    curr_ts = pendulum.parse(templates_dict['curr']).in_tz(tz='Asia/Singapore')
    prev_ts = pendulum.parse(templates_dict['prev']).in_tz(tz='Asia/Singapore')

    logging.info(f'--------Scanning articles from {prev_ts} -> {curr_ts}--------\n')
    new_articles = _searchArticles(curr_ts, prev_ts)
    article_schema = ArticleSchema()

    try:
        for article in new_articles:
            db.session.add(article_schema.load(article))
        db.session.commit()
        logging.info(f'{len(new_articles)} new articles added to database successfully.')
        ti.xcom_push(key='new_articles', value=new_articles)
    except Exception as err:
        print(err)

    return

def sendToTelegram(ti):
    articles = ti.xcom_pull(key='new_articles', task_ids='search_articles')
    users = ti.xcom_pull(key='return_value', task_ids='select_query_user')
    article_schema = ArticleSchema()
    for user in users:
        logging.info(f'Sending message to {user[1]}...')
        chat_id = user[0]
        method = 'sendPhoto'
        url = 'https://api.telegram.org/bot{}/{}'.format(getToken(), method)
        success_counter = 0

        for article in articles:
            params = {
                'chat_id': chat_id,
                'parse_mode': 'HTML',
                **article_schema.load(article).to_payload
            }
            response = requests.post(url=url, params=params)
            if response.ok:
                success_counter += 1
            else:
                logging.info(f'{article["name"]} not sent to {user[1]}...')
        
        if success_counter == len(articles):
            logging.info(f'All messages successfully sent!')
        else:
            logging.info(f'{success_counter}/{len(articles)} messages sent! Some messages not sent...')

if __name__ =='__main__':
    # searchArticles()
    # test_sendPic()
    pass
