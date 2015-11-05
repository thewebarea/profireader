from ..constants.TABLE_TYPES import TABLE_TYPES
from sqlalchemy import Column, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship, backref
from ..controllers import errors
from flask import g
from utils.db_utils import db
#from .portal import Portal
# from .articles import ArticlePortalDivision
from .pr_base import PRBase, Base


# TODO (AA to AA): Add constraint: name shouldn't start or end with blank
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


# TODO (AA to AA): First of all make transform TagCompany -> TagPortal in real DB
# TODO (AA to AA): We have to add a trigger that check the intersection of tags from
# TODO (AA to AA) TagPortal and TagPortalDivision. This intersection must be empty.
class TagPortal(Base, PRBase):
    """ This table contains ONLY portal tags not bound to any division"""
    __tablename__ = 'tag_portal'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
    tag_id = Column(TABLE_TYPES['id_profireader'],
                    ForeignKey(Tag.id, onupdate='CASCADE', ondelete='CASCADE'),
                    nullable=False)
    portal_id = Column(TABLE_TYPES['id_profireader'],
                       ForeignKey('portal.id', onupdate='CASCADE', ondelete='CASCADE'),
                       nullable=False)

    tag = relationship('Tag')

    UniqueConstraint('tag_id', 'portal_id', name='uc_tag_id_company_id')

    def __init__(self, tag_id=None, portal_id=None):
        super(TagPortal, self).__init__()
        self.tag_id = tag_id
        self.portal_id = portal_id


class TagPortalDivision(Base, PRBase):
    __tablename__ = 'tag_portal_division'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
    tag_id = Column(TABLE_TYPES['id_profireader'],
                    ForeignKey(Tag.id, onupdate='CASCADE', ondelete='CASCADE'),
                    nullable=False)
    portal_division_id = Column(TABLE_TYPES['id_profireader'],
                                ForeignKey('portal_division.id',
                                           onupdate='CASCADE',
                                           ondelete='CASCADE'),
                                nullable=False)

    UniqueConstraint('tag_id', 'portal_division_id', name='uc_tag_id_portal_division_id')
    # UniqueConstraint('position', 'portal_division_id', name='uc_position_portal_division_id')
    # there is an additional constraint implemented in DB via trigger:
    # tag position have to be unique within portal.

    tag = relationship('Tag', back_populates='portal_divisions_assoc')
    portal_division = relationship('PortalDivision', back_populates='tags_assoc')
    articles = relationship('ArticlePortalDivision', secondary='tag_portal_division_article',
                            back_populates='article_portal_division_tags', lazy='dynamic')

    def __init__(self, tag_id=None, portal_division_id=None):
        super(TagPortalDivision, self).__init__()
        self.tag_id = tag_id
        self.portal_division_id = portal_division_id

    # def validate(self, tag_name):
    #     ret = {'errors': {}, 'warnings': {}, 'notices': {}}
    #
    #     if tag_name == '':
    #         ret['errors']['name'] = 'empty tag is not allowed'
    #
    #     portal_bound_tags_dynamic = db(Portal, id=self.portal_division.portal_id).portal_bound_tags_dynamic
    #     portal_bound_tag_names = map(lambda obj: getattr(obj, 'name'), portal_bound_tags_dynamic)
    #     if tag_name in portal_bound_tag_names:
    #         ret['errors']['name'] = 'this portal tag already exists'
    #
    #     return ret


class TagPortalDivisionArticle(Base, PRBase):
    __tablename__ = 'tag_portal_division_article'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
    article_portal_division_id = Column(TABLE_TYPES['id_profireader'],
                                        ForeignKey('article_portal_division.id'),
                                        nullable=False)
    tag_portal_division_id = Column(TABLE_TYPES['id_profireader'],
                                    ForeignKey('tag_portal_division.id'),
                                    nullable=False)

    article_portal_division = relationship('ArticlePortalDivision', backref=backref('tag_assoc', lazy='dynamic'))
    tag = relationship('TagPortalDivision', backref=backref('article_assoc', lazy='dynamic'))
#     TODO: many to (many to many)...
    UniqueConstraint('article_portal_division_id', 'tag_portal_division_id', name='uc_article_tag_id')


# class KeyWords(Base, PRBase):

