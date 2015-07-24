from db_connect import metadata
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Binary, Float, TIMESTAMP
from sqlalchemy.orm import mapper

files_table = Table('files', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('parent_id', Integer),
                    Column('name', String(100)),
                    Column('mime', String(30)),
                    Column('content', Binary),
                    Column('size', Float),
                    Column('user_id', Integer, ForeignKey('user.id')),
                    Column('cr_tm', TIMESTAMP),
                    Column('md_tm', TIMESTAMP),
                    Column('ac_tm', TIMESTAMP)
                    )
class Files(object):

    def __init__(self, parent_id=None, name=None, mime=None, content=None, size=None, user_id=None, cr_tm=None, md_tm=None, ac_tm=None):
        self.parent_id = parent_id
        self.name = name
        self.mime = mime
        self.content = content
        self.size = size
        self.user_id = user_id
        self.cr_tm = cr_tm
        self.md_tm = md_tm
        self.ac_tm = ac_tm
mapper(Files, files_table)
