from ..constants.TABLE_TYPES import TABLE_TYPES
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from ..controllers import errors
from flask import g
from utils.db_utils import db
from .company import Company
from .portal import PortalDivision
from .pr_base import PRBase, Base


class Tag(Base, PRBase):
    __tablename__ = 'tag'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
    name = Column(TABLE_TYPES['short_name'])

    def __init__(self, name=None):
        super(Tag, self).__init__()
        self.name = name


class TagPortalDivision(Base, PRBase):
    __tablename__ = 'tag_portal_division'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
    tag_id = Column(TABLE_TYPES['id_profireader'], ForeignKey(Tag.id), nullable=False)
    portal_division_id = Column(TABLE_TYPES['id_profireader'],
                                ForeignKey('portal_division.id'),
                                nullable=False)

    def __init__(self, tag_id=None, portal_division_id=None):
        super(TagPortalDivision, self).__init__()
        self.tag_id = tag_id
        self.portal_division_id = portal_division_id
