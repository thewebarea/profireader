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
    def getTranslate(template, phrase):
        tr =[b for b in db(TranslateTemplate, template=template, name=phrase)]
        if tr:
            phrase = tr[0]
        else:
            return ''
        return phrase.uk

    @staticmethod
    def saveTranslate(template, name, uk, en):
        if TranslateTemplate.isExist(template, name):
            return 'null'
        else:
            tr = TranslateTemplate(template=template,
                          name=name,
                          uk=uk,
                          en=en).save()
            return tr.name

    @staticmethod
    def isExist(template, phrase):
        list = [f for f in db(TranslateTemplate, template=template, name=phrase)]
        return True if list else False
