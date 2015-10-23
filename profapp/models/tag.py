from ..constants.TABLE_TYPES import TABLE_TYPES
from sqlalchemy import Column, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship, backref
from ..controllers import errors
from flask import g
from utils.db_utils import db
from .company import Company
#from .portal import Portal
# from .articles import ArticlePortal
from .pr_base import PRBase, Base


class Tag(Base, PRBase):
    __tablename__ = 'tag'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
    name = Column(TABLE_TYPES['short_name'], index=True, unique=True)

    portal_divisions_assoc = relationship('TagPortalDivision', back_populates='tag')

    def __init__(self, name=None):
        super(Tag, self).__init__()
        self.name = name

    def attach(self):
        pass

    def remove(self):
        pass

    def delete(self):
        pass


class TagCompany(Base, PRBase):
    __tablename__ = 'tag_company'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
    tag_id = Column(TABLE_TYPES['id_profireader'],
                    ForeignKey(Tag.id, onupdate='CASCADE', ondelete='CASCADE'),
                    nullable=False)
    company_id = Column(TABLE_TYPES['id_profireader'],
                        ForeignKey(Company.id, onupdate='CASCADE', ondelete='CASCADE'),
                        nullable=False)
    position = Column(TABLE_TYPES['int'],
                      CheckConstraint('position >= 1', name='cc_position'),
                      nullable=False)

    UniqueConstraint('tag_id', 'company_id', name='uc_tag_id_company_id')
    UniqueConstraint('position', 'company_id', name='uc_position_company_id')


class TagPortalDivision(Base, PRBase):
    __tablename__ = 'tag_portal_division'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
    tag_id = Column(TABLE_TYPES['id_profireader'],
                    ForeignKey(Tag.id, onupdate='CASCADE', ondelete='CASCADE'),
                    nullable=False)
    position = Column(TABLE_TYPES['int'],
                      CheckConstraint('position >= 1', name='cc_position'),
                      nullable=False)
    portal_division_id = Column(TABLE_TYPES['id_profireader'],
                                ForeignKey('portal_division.id',
                                           onupdate='CASCADE',
                                           ondelete='CASCADE'),
                                nullable=False)

    UniqueConstraint('tag_id', 'portal_division_id', name='uc_tag_id_portal_division_id')
    UniqueConstraint('position', 'portal_division_id', name='uc_position_portal_division_id')
    # there is an additional constraint implemented in DB via trigger:
    # tag position have to be unique within portal.

    tag = relationship('Tag', back_populates='portal_divisions_assoc')
    portal_division = relationship('PortalDivision', back_populates='tags_assoc')
    articles = relationship('ArticlePortal', secondary='tag_portal_division_article',
                            back_populates='article_portal_tags', lazy='dynamic')
    # tag_company = relationship('TagCompany',
    #                            back_populates='tag_portal_division',
    #                            primaryjoin='TagPortalDivision.portal_division_id == remote(PortalDivision.id)',
    #                            secondaryjoin='PortalDivision.portal_id == remote(Portal.id)',
    #                            secondaryjoin='Portal.company_owner_id == remote(Company)',
    #                            uselist=False)

    # SELECT * FROM TagPortalDivision LEFT JOIN PortalDivision ON (TagPortalDivision.portal_division_id = PortalDivision.id)
    # TagCompany.company_id == TagPortalDivision.portal_division_id

    def __init__(self, tag_id=None, portal_division_id=None, position=1):
        super(TagPortalDivision, self).__init__()
        self.position = position
        self.tag_id = tag_id
        self.portal_division_id = portal_division_id

    # def validate(self, tag_name):
    #     ret = {'errors': {}, 'warnings': {}, 'notices': {}}
    #
    #     if tag_name == '':
    #         ret['errors']['name'] = 'empty tag is not allowed'
    #
    #     portal_tags = db(Portal, id=self.portal_division.portal_id).portal_tags
    #     portal_tag_names = map(lambda obj: getattr(obj, 'name'), portal_tags)
    #     if tag_name in portal_tag_names:
    #         ret['errors']['name'] = 'this portal tag already exists'
    #
    #     return ret


class TagPortalDivisionArticle(Base, PRBase):
    __tablename__ = 'tag_portal_division_article'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
    article_portal_id = Column(TABLE_TYPES['id_profireader'],
                               ForeignKey('article_portal.id'),
                               nullable=False)
    tag_portal_division_id = Column(TABLE_TYPES['id_profireader'],
                                    ForeignKey('tag_portal_division.id'),
                                    nullable=False)

    article_portal = relationship('ArticlePortal', backref=backref('tag_assoc', lazy='dynamic'))
    tag = relationship('TagPortalDivision', backref=backref('article_assoc', lazy='dynamic'))
#     TODO: many to (many to many)...
    UniqueConstraint('article_portal_id', 'tag_portal_division_id', name='uc_article_tag_id')


# class KeyWords(Base, PRBase):

