import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Database.models import Article, User
from Database.models import db      # copy of Database/models.py pointintg at new DB

if __name__ == '__main__':
    articles = Article.query.all()
    users = User.query.all()

    def get_kwargs(obj):
        _ = vars(obj)
        _.pop('_sa_instance_state')
        return _

    # db.create_all()
    for article in articles:
        db.session.add(Article(**get_kwargs(article)))

    for user in users:
        db.session.add(User(**get_kwargs(user)))
    
    input()
    db.session.commit()
