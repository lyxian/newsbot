from bs4 import BeautifulSoup
from datetime import datetime
import requests

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Database.models import Article, ArticleSchema

def searchArticles():   # WIP
    # Get latest article in DB
    # Get recent articles from WEB
    # Append to DB
    
    def _check_name(response, name):
        return name in [i['name'] for i in response]
        
    latest_article = Article.query.order_by(Article.date.desc())[5]
    articles = content()
    found = False

    if _check_name(articles, latest_article.name):
        found = True

    if found:
        names = [article['name'] for article in articles]
        end = names.index(latest_article.name)
        
        # Remove duplicates in list of dictionary
        new_articles = sorted([dict(t) for t in {tuple(d.items()) for d in articles[:end]}], key=lambda _: _['date'], reverse=False)
        
        return new_articles, '\n', vars(latest_article)

        try:
            for article in new_articles:
                schema = ArticleSchema()
                db.session.add(schema.load(article))
            db.session.commit()
            logging.info(f'{len(new_articles)} new articles added to database successfully.')
            ti.xcom_push(key='new_articles', value=new_articles)
        except Exception as err:
            print(err)
    else:
        return
        if True:
            # Remove duplicates in list of dictionary
            articles = [dict(t) for t in {tuple(d.items()) for d in articles}]
            
            try:
                for article in articles:
                    schema = ArticleSchema()
                    db.session.add(schema.load(article))
                db.session.commit()
                logging.info(f'{len(articles)} new articles added to database successfully.')
                ti.xcom_push(key='new_articles', value=articles)
            except Exception as err:
                print(err)
        else:
            print('not found')
            logging.info('Latest article not found...\nPlease check again...')
    return

def content():
    url = 'https://www.mothership.sg'
    response = requests.get(url)
    content = BeautifulSoup(response.content, 'html.parser')
    latest_news = content.find('div', {'id': 'latest-news'}).find_all('div', {'class': 'ind-article'})
    return [_html_to_json(news) for news in latest_news]

# url, image_url, title (h1), excerpt (subtitle), date, name (url's params)
def _html_to_json(tag):
    url = tag.find('a').attrs['href']
    return {
        'date': tag.find('span').text,
        'excerpt': tag.find('p', {'class': 'subtitle'}).text,
        'image_url': tag.find('div', {'class': 'featured-image'}).attrs['style'].split('url')[-1][2:-2],
        'name': url.split('/')[-2],
        'title': tag.find('h1').text,
        'url': url
    }

# num VARIES from 1-6
def content_more(num):
    headers = {
        'referer': 'https://mothership.sg/',
    }
    url = 'https://www.mothership.sg/json/posts-{}.json'.format(num)
    response = requests.get(url, headers=headers)
    records = _include_year(response.json())
    return records

from typing import List
def _include_year(record_json: List[dict]):
    import re
    for record in record_json:
        year = re.search('\\d{4}', record['url']).group()
        date = record['date'].split(', ')
        date.insert(1, year)
        record['date'] = ', '.join(date)
    return record_json

def _get_user_prop(message_json: dict):
    return {
        'chat_id': message_json['from']['id'],
        'username': message_json['from']['username'],
        'first_name': message_json['from']['first_name'],
        'date_joined': datetime.fromtimestamp(message_json['date']).isoformat()
    }

if __name__ == '__main__':
    pass