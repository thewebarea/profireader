from ..constants.TABLE_TYPES import TABLE_TYPES
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from ..controllers import errors
from flask import g
from utils.db_utils import db
from .company import Company
from .portal import PortalDivision
# from .articles import ArticlePortal
from .pr_base import PRBase, Base


class Tag(Base, PRBase):
    __tablename__ = 'tag'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
    name = Column(TABLE_TYPES['short_name'])

    def __init__(self, name=None):
        super(Tag, self).__init__()
        self.name = name

    def attach(self):
        pass

    def remove(self):
        pass

    def delete(self):
        pass


# class TagPortalDivision(Base, PRBase):
#     __tablename__ = 'tag_portal_division'
#     id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
#     tag_id = Column(TABLE_TYPES['id_profireader'], ForeignKey(Tag.id), nullable=False)
#     portal_division_id = Column(TABLE_TYPES['id_profireader'],
#                                 ForeignKey('portal_division.id'),
#                                 nullable=False)
#     articles = relationship('ArticlePortal', secondary='TagPortalDivisionArticle',
#                             backref=backref('tags', lazy='dynamic'), lazy='dynamic')
#
#     def __init__(self, tag_id=None, portal_division_id=None):
#         super(TagPortalDivision, self).__init__()
#         self.tag_id = tag_id
#         self.portal_division_id = portal_division_id


# class TagPortalDivisionArticle(Base, PRBase):
#     __tablename__ = 'tag_portal_division'
#     id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
#     article_portal_id = Column(TABLE_TYPES['id_profireader'],
#                                ForeignKey(ArticlePortal.id),
#                                nullable=False)
#     tag_portal_division_id = Column(TABLE_TYPES['id_profireader'],
#                                     ForeignKey(TagPortalDivision.id),
#                                     nullable=False)
#     cr_tm = Column(TABLE_TYPES['timestamp'])
#
#     article = relationship('ArticlePortal', backref=backref('tag_assoc', lazy='dynamic'))
#     tag = relationship('TagPortalDivision', backref=backref('article_assoc', lazy='dynamic'))
#     TODO: many to many to many...
#     UniqueConstraint('article_portal_id', 'tag_portal_division_id', name='uc_article_tag_id')

    # employers = relationship('Company', secondary='user_company',
    #                          backref=backref("employees", lazy='dynamic'))  # Correct
    # _relationship = relationship('File',
    #                               uselist=False,
    #                               backref='logo_owner_company',
    #                               foreign_keys='Company.logo_file')

# class KeyWords(Base, PRBase):

