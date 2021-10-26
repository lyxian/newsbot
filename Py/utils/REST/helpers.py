from re import search
from bs4 import BeautifulSoup
from datetime import datetime
import requests

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Database.models import Article, ArticleSchema

def _searchArticles(curr, prev):
    def _check_name(response, name):
        return name in [i['name'] for i in response]
        
    latest_article = Article.query.order_by(Article.date.desc()).first()
    articles = content()
    found = False

    if _check_name(articles, latest_article.name):
        found = True
    else:
        for num in range(1,7):
            new_articles = content_more(num)
            articles.extend(new_articles)
            if _check_name(new_articles, latest_article.name):
                # print(num)
                found = True
                break

    # Include only new articles
    if found:
        names = [article['name'] for article in articles]
        end = names.index(latest_article.name)
        articles = articles[:end]
        
    # Modify <article> to have timestamp
    for article in articles:
        article['timestamp'] = datetime.strptime(article['date'], '%B %d, %Y, %I:%M %p').timestamp()

    # Remove duplicates in list of dictionary
    new_articles = sorted([dict(t) for t in {tuple(d.items()) for d in articles}], key=lambda _: _['timestamp'], reverse=False)
    
    # Filter by 'curr'/'prev' time
    prev = prev.timestamp() # pendulum.parse(prev).in_tz(tz='Asia/Singapore').timestamp()
    curr = curr.timestamp() # pendulum.parse(curr).in_tz(tz='Asia/Singapore').timestamp()

    return [article for article in new_articles if prev < article['timestamp'] <= curr]

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
    print(_searchArticles())
    pass