from sqlalchemy import Table, Column, Integer, Text, ForeignKey, String, Boolean, func, desc
from sqlalchemy.orm import relationship, backref, aliased


from ..constants.TABLE_TYPES import TABLE_TYPES
from ..constants.STATUS import STATUS
from db_init import db_session
from ..models.company import Company
from ..models.users import User


from ..controllers.errors import BadDataProvided

from flask import g
from .pr_base import PRBase
from db_init import Base


def _Q(cls):
    return db_session.query(cls)


def _A():
    return db_session.query(Article)


def _C():
    return db_session.query(ArticleCompany)


class ArticleCompany(Base, PRBase):
    __tablename__ = 'article_company'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True, info={'visible': True})

    editor_user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'), nullable=False, info={'visible': True})
    company_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company.id'), info={'visible': True})
    article_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('article.id'), info={'visible': True})
    # created_from_version_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('article_version.id'))

    title = Column(TABLE_TYPES['title'], nullable=False, info={'visible': True})
    short = Column(TABLE_TYPES['text'], nullable=False, info={'visible': True})
    long = Column(TABLE_TYPES['text'], nullable=False, info={'visible': True})

    cr_tm = Column(TABLE_TYPES['timestamp'], info={'visible': True})
    md_tm = Column(TABLE_TYPES['timestamp'], info={'visible': True})

    company = relationship(Company)
    editor = relationship(User)
    # article = relationship('Article')

    def clone_for_company(self, company_id):
        return self.detach().attr({'company_id': company_id}).save()


class Article(Base, PRBase):
    __tablename__ = 'article'

    id = Column(TABLE_TYPES['id_profireader'], primary_key=True, info={'visible': True})
    author_user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'), nullable=False, info={'visible': True})

    submitted = relationship(ArticleCompany, primaryjoin="and_(Article.id==ArticleCompany.article_id, ArticleCompany.company_id!=None)", info={'visible': True})
    mine = relationship(ArticleCompany, primaryjoin="and_(Article.id==ArticleCompany.article_id, ArticleCompany.company_id==None)", uselist=False, info={'visible': True})

    @staticmethod
    def save_new_article(user_id, **kwargs):
        article = Article(mine = ArticleCompany(editor_user_id = user_id, company_id=None, **kwargs),
            author_user_id = user_id)
        return article.save()

    @staticmethod
    def save_edited_version(user_id, article_company_id, **kwargs):
        return ArticleCompany.get(article_company_id).attr(kwargs).save()

    @staticmethod
    def user_articles(user_id=None, before_id=None):
        return _A().filter_by(author_user_id=user_id).all()



