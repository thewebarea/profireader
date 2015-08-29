from sqlalchemy import Table, Column, Integer, Text, ForeignKey, String, Boolean, func, desc
from sqlalchemy.orm import relationship, backref, aliased

from ..constants.TABLE_TYPES import TABLE_TYPES
from db_init import db_session
from ..models.company import Company
from ..models.users import User
from utils.db_utils import db

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

    editor_user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'), nullable=False,
                            info={'visible': True})
    company_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company.id'))
    article_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('article.id'))
    # created_from_version_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('article_version.id'))

    title = Column(TABLE_TYPES['title'], nullable=False)
    short = Column(TABLE_TYPES['text'], nullable=False)
    long = Column(TABLE_TYPES['text'], nullable=False)

    status = Column(TABLE_TYPES['status'], nullable=False)

    cr_tm = Column(TABLE_TYPES['timestamp'])
    md_tm = Column(TABLE_TYPES['timestamp'])

    company = relationship(Company)
    editor = relationship(User)
    # article = relationship('Article')

    def clone_for_company(self, company_id):
        return self.detach().attr({'company_id': company_id}).save()


class Article(Base, PRBase):
    __tablename__ = 'article'

    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    author_user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'), nullable=False,
                            info={'visible': True})

    submitted = relationship(ArticleCompany,
                             primaryjoin="and_(Article.id==ArticleCompany.article_id, ArticleCompany.company_id!=None)",
                             info={'visible': True})
    mine = relationship(ArticleCompany,
                        primaryjoin="and_(Article.id==ArticleCompany.article_id, ArticleCompany.company_id==None)",
                        uselist=False)

    def get_client_side_dict(self):
        return self.to_dict('id, mine|submitted.id|title|short|cr_tm|md_tm|company_id|status, submitted.editor.id|profireader_name, submitted.company.name')

    @staticmethod
    def save_new_article(user_id, **kwargs):
        article = Article(mine=ArticleCompany(editor_user_id=user_id, company_id=None, **kwargs),
                          author_user_id=user_id)
        return article.save()

    @staticmethod
    def search_for_company_to_submit(user_id, article_id, searchtext):
        return [x.to_dict('id,name') for x in db(Company)
#TODO: AA by OZ:    .filter(user_id has to be employee in company and must have rights to submit article to this company)
            .filter(~db(ArticleCompany).filter_by(company_id=Company.id, article_id=article_id).exists()) # article is NOT published yet in company
            .filter(Company.name.like("%" + searchtext + "%")).all()]

    @staticmethod
    def save_edited_version(user_id, article_company_id, **kwargs):
        return ArticleCompany.get(article_company_id).attr(kwargs).save()

    @staticmethod
    def user_articles(user_id=None, before_id=None):
        return _A().filter_by(author_user_id=user_id).all()
