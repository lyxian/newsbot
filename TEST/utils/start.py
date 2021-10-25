# This module initializes a temporary database for testing
# - run this module with <num> to choose the n-th latest article

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Py.utils.SQLite.query import sql_query, sql_table_columns
from TEST.utils.models import db, Article, ArticleSchema
from datetime import datetime

# Constants
count = 1
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
destFile = 'TEST/data/test.db'
destPath = os.path.join(base_dir, destFile)
destDir = os.path.dirname(destPath)
sourcePath = os.path.join(base_dir, 'data/articles.db')


def _get_latest_article(num: int):
    cmd = f'SELECT * FROM article ORDER BY date DESC LIMIT {num}'
    if num != 1:
        latest_article = sql_query(sourcePath, cmd)[-1]
    else:
        latest_article = sql_query(sourcePath, cmd)
    columns = sql_table_columns(sourcePath, 'article')
    obj = {k:v for k,v in zip(columns, latest_article)}
    obj['date'] = datetime.strptime(obj['date'], '%Y-%m-%d %H:%M:%S.%f').strftime('%B %d, %Y, %I:%M %p')

    return ArticleSchema().load(obj)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        count = sys.argv[1]
    
    if 1:
        if os.path.exists(destPath):
            os.remove(destPath)
        db.create_all()
        db.session.add(_get_latest_article(count))
        db.session.commit()

        print(Article.query.all())