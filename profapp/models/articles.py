from sqlalchemy import Table, Column, Integer, Text, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, backref

from db_init import Base
from ..constants.TABLE_TYPES import TABLE_TYPES
from ..constants.STATUS import STATUS
from db_init import db_session

from flask import g

def _A():
    return db_session.query(Article)

def _V():
    return db_session.query(ArticleVersion)


class Article(Base):
    __tablename__ = 'article'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)


    def __init__(self, id = None):
        self.id = id

    @staticmethod
    def list(user_id=None, before_id = None):
        ret = _A().all()
        return ret

    @staticmethod
    def get_versions(article_id=None):
        return _A().filter(Article.id == article_id).one().versions

    @staticmethod
    def get_one_version(article_version_id=None):
        return _V().filter(ArticleVersion.id == article_version_id).one()

class ArticleVersion(Base):

    __tablename__ = 'article_version'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)

    author_user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'), nullable=False)
    company_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company.id'))
    created_from_version_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('article_version.id'))
    article_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('article.id'))

    name =  Column(TABLE_TYPES['name'], nullable=False)
    short =  Column(TABLE_TYPES['text'], nullable=False)
    long =  Column(TABLE_TYPES['text'], nullable=False)

    article = relationship('Article', backref=backref('versions', order_by='desc(ArticleVersion.id)'))

    def __init__(self, created_from_version_id, author_user_id=None, company_id=None, name='', short='', long=''):

        self.author_user_id = author_user_id if author_user_id is not None else g.user_dict['id']

        self.name = name
        self.short = short
        self.long = long
        self.article = Article() if created_from_version_id is None else _A().filter(Article.id == Article.get_one_version(created_from_version_id).article_id).one()

    def save(self):
        db_session.add(self)
        db_session.commit()
        return self



    def create(self):
        pass


    # def articles_for_user(user_id = g., after_id = None, search = None, count = 10):
    #     articles = db_session.query(Article).filter_by(author_user_id=id, ).all()
    #     return articles
