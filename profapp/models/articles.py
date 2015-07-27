from sqlalchemy import Table, Column, Integer, Text, ForeignKey, String, \
    Boolean
from db_init import Base

class ArticleHistory(Base):
    __tablename__ = 'article_history'
    id = Column(Integer, primary_key=True)
    article_text = Column(Text)
    status = Column(Integer)
    contributor_user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, name, article_text, status, contributor_user_id):
        self.name = name
        self.article_text = article_text
        self.status = status
        self.contributor_user_id = contributor_user_id

class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    author_user_id = Column(Integer, ForeignKey('user.id'))
    company_id = Column(Integer, ForeignKey('company.id'))

    def __init__(self, author_user_id, company_id):
        self.author_user_id = author_user_id
        self.company_id = company_id
