from bs4 import BeautifulSoup
from datetime import datetime
import requests

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
    url = 'https://www.mothership.sg/json/posts-{}.json'.format(num)
    response = requests.get(url)
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