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


def _C():
    return db_session.query(ArticleCompany)


class ArticleCompany(Base, PRBase):
    __tablename__ = 'article_company'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)

    editor_user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'), nullable=False)
    company_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company.id'))
    article_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('article.id'))
    # created_from_version_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('article_version.id'))

    title = Column(TABLE_TYPES['title'], nullable=False)
    short = Column(TABLE_TYPES['text'], nullable=False)
    long = Column(TABLE_TYPES['text'], nullable=False)

    cr_tm = Column(TABLE_TYPES['timestamp'])
    md_tm = Column(TABLE_TYPES['timestamp'])

    company = relationship('Company')
    article = relationship('Article')



    # def __init__(self, created_from_version_id, author_user_id=None, company_id=None, name='', short='', long=''):
    #     self.author_user_id = author_user_id if author_user_id is not None else g.user_dict['id']
    #
    #     self.title = title
    #     self.short = short
    #     self.long = long
    #     self.article = Article() if company_id is None else _A().filter(Article.id == ArticleCompany.get(created_from_version_id).article_id).one()


    def clone_for_company(self, company_id):
        self.detach()
        self.company_id = company_id
        self.created_from_version_id = self.id
        return self


class Article(Base, PRBase):
    __tablename__ = 'article'

    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    author_user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'), nullable=False)

    submitted = relationship('ArticleCompany', primaryjoin="and_(Article.id==ArticleCompany.article_id, ArticleCompany.company_id!=None)")
    mine = relationship('ArticleCompany', primaryjoin="and_(Article.id==ArticleCompany.article_id, ArticleCompany.company_id==None)", uselist=False)

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



# SELECT DISTINCT ON (article_version.company_id) article_version.*, per_group.count FROM article_version LEFT JOIN (SELECT company_id, count(id) as count FROM article_version
# GROUP BY article_version.company_id) as per_company  ON
# (per_company.company_id = article_version.company_id OR (per_group.company_id IS NULL AND article_version.company_id IS NULL))
# ORDER BY company_id, id


        return _A().filter_by(author_user_id=user_id).all()

    @staticmethod
    def get_last_company_versions_for_user(article_id, author_user_id):
        # grouped_by_company = aliased(ArticleVersion)
        # grouped_by_company_subquery = db_session.query(ArticleVersion.company_id).filter_by(article_id=article_id, author_user_id=author_user_id).group_by(ArticleVersion.company_id).subquery()
        # ret = db_session.query(ArticleVersion).distinct('article_version.company_id').filter_by(article_id=article_id, author_user_id=author_user_id).order_by(ArticleVersion.company_id, desc(ArticleVersion.id)).outerjoin(grouped_by_company_subquery, grouped_by_company_subquery.c.company_id == ArticleVersion.company_id)
        # ret = ret.all()
        return []


