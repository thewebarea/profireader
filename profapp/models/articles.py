from sqlalchemy import Table, Column, Integer, Text, ForeignKey, String, \
    Boolean
from db_init import Base
from ..constants.TABLE_TYPES import TABLE_TYPES
from ..constants.STATUS import STATUS
from db_init import db_session

class ArticleHistory(Base):
    __tablename__ = 'article_history'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    article_text = Column(TABLE_TYPES['text_long'])
    contributor_user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'))
    status = Column(Integer)

    def __init__(self, name, article_text, contributor_user_id, status):
        self.name = name
        self.article_text = article_text
        self.status = status
        self.contributor_user_id = contributor_user_id


class Article(Base):
    __tablename__ = 'article'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    author_user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'), nullable=False)
    company_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company.id'), nullable=False)

    def __init__(self, author_user_id, company_id):
        self.author_user_id = author_user_id
        self.company_id = company_id

    def query_all_articles(id):

        status = STATUS()
        articles = db_session.query(Article).filter_by(author_user_id=id).all()

        return articles
