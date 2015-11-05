from sqlalchemy import Column
from ..constants.TABLE_TYPES import TABLE_TYPES
from .pr_base import PRBase, Base


class Config(Base, PRBase):
    __tablename__ = 'config'
    id = Column(TABLE_TYPES['name'], primary_key=True, nullable=False)
    value = Column(TABLE_TYPES['text'])
    type = Column(TABLE_TYPES['name'])
    comment = Column(TABLE_TYPES['text'])
    client_side = Column(TABLE_TYPES['boolean'])
    server_side = Column(TABLE_TYPES['boolean'])

