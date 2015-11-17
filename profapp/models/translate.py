from .pr_base import PRBase, Base
from ..constants.TABLE_TYPES import TABLE_TYPES
from sqlalchemy import Column, ForeignKey, text
from utils.db_utils import db

class TranslateTemplate(Base, PRBase):
    __tablename__ = 'translate'

    id = Column(TABLE_TYPES['id_profireader'], primary_key=True, nullable=False)
    template = Column(TABLE_TYPES['short_name'], default='')
    name = Column(TABLE_TYPES['name'], default='')
    uk = Column(TABLE_TYPES['name'], default='')
    en = Column(TABLE_TYPES['name'], default='')

    def __init__(self, id=None, template=None, name=None, uk=None, en=None):
        self.id = id
        self.template = template
        self.name = name
        self.uk = uk
        self.en = en


    @staticmethod
    def getTranslate(template):
        tr = list({'name': file.name,
                   'uk': file.uk,
                   'en':file.en
                   }
                  for file in db(TranslateTemplate, template=template))
        return tr

    @staticmethod
    def saveTranslate(template, name, uk, en):
        return TranslateTemplate(template=template,
                          name=name,
                          uk=uk,
                          en=en).save()
