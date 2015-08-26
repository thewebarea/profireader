from sqlalchemy import Table, Column, Integer, Text, ForeignKey, String, Boolean, func, desc
from sqlalchemy.orm import relationship, backref, aliased


from ..constants.TABLE_TYPES import TABLE_TYPES
from ..constants.STATUS import STATUS
from db_init import db_session


from ..controllers.errors import BadDataProvided

from flask import g
from .pr_base import PRBase
from db_init import Base


def _Q(cls):
    return db_session.query(cls)


def _A():
    return db_session.query(Article)


def _V():
    return db_session.query(ArticleVersion)


class ArticleVersion(Base, PRBase):
    __tablename__ = 'article_version'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)

    author_user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'), nullable=False)
    company_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company.id'))
    created_from_version_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('article_version.id'))
    article_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('article.id'))

    name = Column(TABLE_TYPES['name'], nullable=False)
    short = Column(TABLE_TYPES['text'], nullable=False)
    long = Column(TABLE_TYPES['text'], nullable=False)

    article = relationship('Article')
    company = relationship('Company')

    def __init__(self, created_from_version_id, author_user_id=None, company_id=None, name='', short='', long=''):
        self.author_user_id = author_user_id if author_user_id is not None else g.user_dict['id']

        self.name = name
        self.short = short
        self.long = long
        self.article = Article() if created_from_version_id is None else _A().filter(
            Article.id == ArticleVersion.get(created_from_version_id).article_id).one()


    def clone_for_company(self, company_id):
        self.detach()
        self.company_id = company_id
        self.created_from_version_id = self.id
        return self


class Article(Base, PRBase):
    __tablename__ = 'article'
    versions = relationship('ArticleVersion', primaryjoin="Article.id==ArticleVersion.article_id",
                            order_by='desc(ArticleVersion.id)')
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)

    @staticmethod
    def list(user_id=None, company_id=None, before_id=None):

        if user_id is None and company_id is None:
            raise BadDataProvided

        ret = _A()


# SELECT DISTINCT ON (article_version.company_id) article_version.*, per_group.count FROM article_version LEFT JOIN (SELECT company_id, count(id) as count FROM article_version
# GROUP BY article_version.company_id) as per_company  ON
# (per_company.company_id = article_version.company_id OR (per_group.company_id IS NULL AND article_version.company_id IS NULL))
# ORDER BY company_id, id




        if user_id is not None:
            ret = ret.filter(Article.versions.any(author_user_id=user_id))
        if company_id is not None:
            ret = ret.filter(Article.versions.any(company_id=company_id))

        return ret.all()

    @staticmethod
    def get_last_company_versions_for_user(article_id, author_user_id):
        # grouped_by_company = aliased(ArticleVersion)
        grouped_by_company_subquery = db_session.query(ArticleVersion.company_id).filter_by(article_id=article_id, author_user_id=author_user_id).group_by(ArticleVersion.company_id).subquery()
        ret = db_session.query(ArticleVersion).distinct('article_version.company_id').filter_by(article_id=article_id, author_user_id=author_user_id).order_by(ArticleVersion.company_id, desc(ArticleVersion.id)).outerjoin(grouped_by_company_subquery, grouped_by_company_subquery.c.company_id == ArticleVersion.company_id)
        ret = ret.all()
        return ret


