from sqlalchemy import Column, Integer, ForeignKey, String, Binary, Float, TIMESTAMP
from db_init import db_session as db
from db_init import Base

class File(Base):
    __tablename__ = 'file'
    id = Column(String(36), primary_key=True)
    parent_id = Column(String(36))
    name = Column(String(100))
    mime = Column(String(30), default='text/plain')
    content = Column(Binary)
    description = Column(String(1000), default='')
    size = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('user.id'))
    cr_tm = Column(TIMESTAMP)
    md_tm = Column(TIMESTAMP)
    ac_tm = Column(TIMESTAMP)

    def __init__(self, parent_id=None, name=None, mime='text/plain', content=None, size=None, user_id=None, cr_tm=None, md_tm=None, ac_tm=None, company_id=None, copyright='', author=''):
        self.parent_id = parent_id
        self.name = name
        self.mime = mime
        self.content = content
        self.size = size
        self.user_id = user_id
        # if cr_tm: self.cr_tm = cr_tm
        # if cr_tm: self.cr_tm = cr_tm
        # self.md_tm = md_tm
        # self.ac_tm = ac_tm

    def __repr__(self):
        return "<File(name='%s', mime=%s', id='%s', parent_id='%s')>" % (
                                self.name, self.mime, self.id, self.parend_id)

    def is_directory(file_id):
        return db.query(File).filter(id=file_id)[0].mime == 'directory'

    def list(parent_id=None):
        return list({'size': file.size, 'name': file.name, 'id': file.id,
                                'type': 'dir' if file.mime == 'directory' else 'file',
                                'date': str(file.md_tm).split('.')[0]}
                                        for file in db.query(File).filter(File.parent_id == parent_id))

    def createdir(parent_id=None, name=None, company_id=None, copyright='', author=''):
        f = File(parent_id=parent_id, name=name, size=0, company_id=company_id, copyright=copyright, author=author)
        db.add(f)
        db.commit()
        pass
        return True;

    def upload(parent_id=None, file = None):
        return True


