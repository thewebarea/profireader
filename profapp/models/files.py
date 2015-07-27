from sqlalchemy import Column, Integer, ForeignKey, String, Binary, Float, TIMESTAMP
from db_init import Base

class File(Base):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer)
    name = Column(String(100))
    mime = Column(String(30))
    content = Column(Binary)
    size = Column(Float)
    user_id = Column(Integer, ForeignKey('user.id'))
    cr_tm = Column(TIMESTAMP)
    md_tm = Column(TIMESTAMP)
    ac_tm = Column(TIMESTAMP)

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
