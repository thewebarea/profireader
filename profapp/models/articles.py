from sqlalchemy import Table, Column, Integer, Text, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, backref

from db_init import Base
from ..constants.TABLE_TYPES import TABLE_TYPES
from ..constants.STATUS import STATUS
from db_init import db_session

from flask import g

def db():
    return db_session.query(Article)


class Article(Base):
    __tablename__ = 'article'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)


    def __init__(self, id = None):
        self.id = id

    @staticmethod
    def list(user_id=None, before_id = None):
        session.query(A).filter(A.b.any())
        ret = db().filter(ArticleVersion.author_user_id.any())
        return ret

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

    article = relationship('Article', backref=backref('history'))

    def __init__(self, author_user_id, company_id = None, created_from_article_id = None, name = '', short = '', long=''):
        if created_from_article_id ==  None:
            self.article_bulk = Article(created_from_article_id)
            self.created_from_article_id = created_from_article_id
        else:
            self.article_bulk = Article()

        self.author_user_id = author_user_id
        self.company_id = company_id

        self.name = name
        self.short = short
        self.long = long


    def create(self):
        pass


    # def articles_for_user(user_id = g., after_id = None, search = None, count = 10):
    #     articles = db_session.query(Article).filter_by(author_user_id=id, ).all()
    #     return articles
