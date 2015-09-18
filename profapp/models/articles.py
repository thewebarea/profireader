from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.orm import relationship
from ..constants.TABLE_TYPES import TABLE_TYPES
# from db_init import db_session
from ..models.company import Company
from ..models.portal import PortalDivision
from ..models.users import User
from utils.db_utils import db
from .pr_base import PRBase, Base
# from db_init import Base
from utils.db_utils import db
from ..constants.ARTICLE_STATUSES import ARTICLE_STATUS_IN_COMPANY, ARTICLE_STATUS_IN_PORTAL
from utils.html_utils import clean_html_tags
from flask import g
from sqlalchemy.sql import or_

def _Q(cls):
    return g.db.query(cls)


def _A():
    return g.db.query(Article)


def _C():
    return g.db.query(ArticleCompany)


def _P():
    return g.db.query(ArticlePortal)


class ArticlePortal(Base, PRBase):
    __tablename__ = 'article_portal'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True,
                nullable=False)
    cr_tm = Column(TABLE_TYPES['timestamp'])
    article_company_id = Column(TABLE_TYPES['id_profireader'],
                                ForeignKey('article_company.id'))
    title = Column(TABLE_TYPES['name'], default='')
    short = Column(TABLE_TYPES['text'], default='')
    long = Column(TABLE_TYPES['text'], default='')
    md_tm = Column(TABLE_TYPES['timestamp'])
    publishing_tm = Column(TABLE_TYPES['timestamp'])
    status = Column(TABLE_TYPES['id_profireader'],
                    default=ARTICLE_STATUS_IN_PORTAL.published)
    portal_id = Column(TABLE_TYPES['id_profireader'],
                       ForeignKey('portal.id'))

    image_file_id = Column(TABLE_TYPES['id_profireader'],
                            ForeignKey('file.id'), nullable=False)

    portal_division_id = Column(TABLE_TYPES['id_profireader'],
                                ForeignKey('portal_division.id'))

    division = relationship('PortalDivision', backref='article_portal')

    company = relationship(Company, secondary='article_company',
                           primaryjoin="ArticlePortal.article_company_"
                                       "id == ArticleCompany.id",
                           secondaryjoin="ArticleCompany.company_id == "
                                         "Company.id",
                           viewonly=True, uselist=False)

    def __init__(self, article_company_id=None, title=None, short=None,
                 long=None, status=None, portal_division_id=None, image_file_id = None,
                 portal_id=None):
        self.article_company_id = article_company_id
        self.title = title
        self.short = short
        self.image_file_id = image_file_id
        self.long = long
        self.status = status
        self.portal_division_id = portal_division_id
        self.portal_id = portal_id

    def get_client_side_dict(self, fields='id|image_file_id|title|short|image_file_id|'
                                          'long|cr_tm|md_tm|'
                                          'status|publishing_tm, '
                                          'company.id|name, division.id|name'):
        return self.to_dict(fields)

    @staticmethod
    def update_article_portal(article_portal_id, **kwargs):
        db(ArticlePortal, id=article_portal_id).update(kwargs)

class ArticleCompany(Base, PRBase):
    __tablename__ = 'article_company'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)

    editor_user_id = Column(TABLE_TYPES['id_profireader'],
                            ForeignKey('user.id'), nullable=False,
                            info={'visible': True})
    company_id = Column(TABLE_TYPES['id_profireader'],
                        ForeignKey('company.id'))
    article_id = Column(TABLE_TYPES['id_profireader'],
                        ForeignKey('article.id'))
    # created_from_version_id = Column(TABLE_TYPES['id_profireader'],
    # ForeignKey('article_version.id'))
    title = Column(TABLE_TYPES['title'], nullable=False)
    short = Column(TABLE_TYPES['text'], nullable=False)
    long = Column(TABLE_TYPES['text'], nullable=False)
    status = Column(TABLE_TYPES['status'], nullable=False)
    cr_tm = Column(TABLE_TYPES['timestamp'])
    md_tm = Column(TABLE_TYPES['timestamp'])
    image_file_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('file.id'), nullable=False)
    company = relationship(Company)
    editor = relationship(User)
    article = relationship('Article', primaryjoin="and_(Article.id==ArticleCompany.article_id)",
                           uselist=False)
    portal_article = relationship('ArticlePortal',
                                  primaryjoin="ArticleCompany.id=="
                                              "ArticlePortal."
                                              "article_company_id",
                                  backref='company_article')

    def get_client_side_dict(self, fields='id|title|short|'
                                          'long|cr_tm|md_tm|company_id|'
                                          'article_id|image_file_id|'
                                          'status, company.name'):
        return self.to_dict(fields)
    
    def clone_for_company(self, company_id):
        return self.detach().attr({'company_id': company_id,
                                   'status': ARTICLE_STATUS_IN_COMPANY.
                                  submitted}).save()

        # self.portal_devision_id = portal_devision_id
        # self.article_company_id = article_company_id
        # self.title = title
        # self.short = short
        # self.long = long
        # self.status = status
    def clone_for_portal(self, division):

        self.portal_article.append(
            ArticlePortal(title=self.title, short=self.short,
                          image_file_id=self.image_file_id,
                          long=self.long, portal_division_id=division,
                          article_company_id=self.id,
                          portal_id=db(PortalDivision, id=division).one().portal_id).save())
        return self

    # def update_article(self, **kwargs):
    #     for key, value in kwargs.items():
    #         self.key = value
    #     self.save()
    #     return self

    def get_article_owner_portal(self, **kwargs):
        return [art_port.division.portal for art_port in self.portal_article if kwargs][0]

    @staticmethod
    def update_article(company_id, article_id, **kwargs):
        db(ArticleCompany, company_id=company_id, id=article_id).update(
            kwargs)


class Article(Base, PRBase):
    __tablename__ = 'article'

    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    author_user_id = Column(TABLE_TYPES['id_profireader'],
                            ForeignKey('user.id'), nullable=False,
                            info={'visible': True})

    submitted = relationship(ArticleCompany,
                             primaryjoin="and_(Article.id=="
                                         "ArticleCompany.article_id, "
                                         "ArticleCompany.company_id!="
                                         "None)",
                             info={'visible': True})
    mine = relationship(ArticleCompany,
                        primaryjoin="and_(Article.id==ArticleCompany."
                                    "article_id, ArticleCompany."
                                    "company_id==None)",
                        uselist=False)

    def get_client_side_dict(self,
                             fields='id, mine|submitted.id|title|short|'
                                    'cr_tm|md_tm|company_id|status|image_file_id, '
                                    'submitted.editor.id|'
                                    'profireader_name, '
                                    'submitted.company.name'):
        return self.to_dict(fields)

    @staticmethod
    def save_new_article(user_id, **kwargs):
        return Article(mine=ArticleCompany(editor_user_id=user_id,
                                              company_id=None,
                                              **kwargs),
                                              author_user_id=user_id).save()

    @staticmethod
    def search_for_company_to_submit(user_id, article_id, searchtext):
        # TODO: AA by OZ:    .filter(user_id has to be employee in company and
        # TODO: must have rights to submit article to this company)
        return [x.to_dict('id,name') for x in db(Company)
                .filter(~db(ArticleCompany).
                        filter_by(company_id=Company.id,
                        article_id=article_id).exists())
                .filter(Company.name.ilike(
                        "%" + searchtext + "%")).all()]

    @staticmethod
    def save_edited_version(user_id, article_company_id, **kwargs):
        a = ArticleCompany.get(article_company_id)
        return a.attr(kwargs).save().article

    @staticmethod
    def get_articles_for_user(user_id):
        return _A().filter_by(author_user_id=user_id).all()

    # @staticmethod
    # def subquery_articles_at_portal(portal_division_id=None, search_text=None):
    #
    #     if not search_text:
    #         sub_query = db(ArticlePortal).order_by('publishing_tm').filter(text(
    #             ' "publishing_tm" < clock_timestamp() ')).filter_by(
    #             portal_division_id=portal_division_id,
    #             status=ARTICLE_STATUS_IN_PORTAL.published)
    #     else:
    #         sub_query = db(ArticlePortal).order_by('publishing_tm').filter(text(
    #             ' "publishing_tm" < clock_timestamp() ')).filter_by(
    #             portal_division_id=portal_division_id,
    #             status=ARTICLE_STATUS_IN_PORTAL.published).filter(
    #             or_(
    #                 ArticlePortal.title.ilike("%" + search_text + "%"),
    #                 ArticlePortal.short.ilike("%" + search_text + "%"),
    #                 ArticlePortal.long.ilike("%" + search_text + "%")))
    #     return sub_query

    @staticmethod
    def subquery_articles_at_portal(search_text=None, **kwargs):

        if not search_text:
            sub_query = db(ArticlePortal, status=ARTICLE_STATUS_IN_PORTAL.published, **kwargs).\
                order_by('publishing_tm').filter(text(' "publishing_tm" < clock_timestamp() '))
        else:
            sub_query = db(ArticlePortal, status=ARTICLE_STATUS_IN_PORTAL.published, **kwargs).\
                order_by('publishing_tm').filter(text(' "publishing_tm" < clock_timestamp() ')).\
                filter(or_(
                    ArticlePortal.title.ilike("%" + search_text + "%"),
                    ArticlePortal.short.ilike("%" + search_text + "%"),
                    ArticlePortal.long.ilike("%" + search_text + "%")))
        return sub_query

    # @staticmethod
    # def get_articles_for_portal(page_size, portal_division_id,
    #                             pages, page=1, search_text=None):
    #     page -= 1
    #     if not search_text:
    #         query = _P().order_by('publishing_tm').filter(text(
    #             ' "publishing_tm" < clock_timestamp() ')).filter_by(
    #             portal_division_id=portal_division_id,
    #             status=ARTICLE_STATUS_IN_PORTAL.published)
    #     else:
    #         query = _P().order_by('publishing_tm').filter(text(
    #             ' "publishing_tm" < clock_timestamp() ')).filter_by(
    #             portal_division_id=portal_division_id,
    #             status=ARTICLE_STATUS_IN_PORTAL.published).filter(
    #             or_(
    #                 ArticlePortal.title.ilike("%" + search_text + "%"),
    #                 ArticlePortal.short.ilike("%" + search_text + "%"),
    #                 ArticlePortal.long.ilike("%" + search_text + "%")))
    #
    #     if page_size:
    #         query = query.limit(page_size)
    #     if page:
    #         query = query.offset(page*page_size) if int(page) in range(
    #             0, int(pages)) else query.offset(pages*page_size)
    #
    #     return query

    @staticmethod
    def get_one_article(article_id):
        article = _C().filter_by(id=article_id).one()
        return article

    @staticmethod
    def get_articles_submitted_to_company(company_id):
        articles = _C().filter_by(company_id=company_id).all()
        return articles if articles else []

     # for article in articles:
     #     article.possible_new_statuses = ARTICLE_STATUS_IN_COMPANY.\
     #         can_user_change_status_to(article.status)


class ArticleCompanyHistory(Base, PRBase):
    __tablename__ = 'article_company_history'
    id = Column(TABLE_TYPES['bigint'], primary_key=True)
    editor_user_id = Column(TABLE_TYPES['id_profireader'])
    company_id = Column(TABLE_TYPES['id_profireader'])
    name = Column(TABLE_TYPES['name'])
    short = Column(TABLE_TYPES['text'], default='')
    long = Column(TABLE_TYPES['text'], default='')
    article_company_id = Column(TABLE_TYPES['id_profireader'])
    article_id = Column(TABLE_TYPES['id_profireader'])

    def __init__(self, editor_user_id=None, company_id=None, name=None,
                 short=None, long=None, article_company_id=None,
                 article_id=None):
        self.editor_user_id = editor_user_id
        self.company_id = company_id
        self.name = name
        self.short = short
        self.long = long
        self.article_company_id = article_company_id
        self.article_id = article_id
