from airflow.hooks.base import BaseHook

from marshmallow import Schema, fields, post_load, EXCLUDE
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import sys
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
database_name = 'data/test.db'
database_path = '/home/lyx/wSpace/Py/local/NewsBot/TEST/data/test.db'

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + database_path # os.path.join(basedir, database_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)
    title = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(120), nullable=False)
    excerpt = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime)
    # timestamp = db.Column(db.Integer)

    def __repr__(self):
        # return '<%s %r>' % (self.__class__.__name__, self.name)
        return '<{} {!r}>'.format(self.__class__.__name__, self.name)

    @staticmethod
    def duplicate(obj):
        return Article(**({k:v for k,v in vars(obj).items() if k != 'id' and k[0] != '_'}))

    @property
    def to_payload(self):
        return {
            'photo': self.image_url,
            'caption': f'''<b>{self.title}</b>\n{self.excerpt}\n<a href="{self.url}">Link Here</a>''',
        }

class ArticleSchema(Schema):
    name = fields.String(required=True) 
    date = fields.DateTime(required=True)
    excerpt = fields.String(required=True)
    image_url = fields.URL(required=True)
    title = fields.String(required=True)
    url = fields.URL(required=True)
    # timestamp = fields.Integer(required=True)
    
    # can include Meta in (parent) BaseSchema
    class Meta:
        datetimeformat = '%B %d, %Y, %I:%M %p'
        unknown = EXCLUDE

    @post_load
    def return_object(self, data, **kwargs):
        return Article(**data)

if __name__ == '__main__':
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    db.create_all()
    pass