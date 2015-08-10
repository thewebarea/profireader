from sqlalchemy import Column, Integer, ForeignKey, String, Binary, Float, TIMESTAMP
from db_init import Base, db_session as db
import re
from ..constants.TABLE_TYPES import USER_TABLE_TYPES

class File(Base):
    __tablename__ = 'file'
    id = Column(String(36), primary_key=True)
    parent_id = Column(String(36))
    name = Column(String(100))
    mime = Column(String(30))

    size = Column(Float)
    user_id = Column(USER_TABLE_TYPES['ID'], ForeignKey('user.id'))
    cr_tm = Column(TIMESTAMP)
    md_tm = Column(TIMESTAMP)
    ac_tm = Column(TIMESTAMP)

    def __init__(self, parent_id=None, name=None, mime='text/plain', size=None, user_id=None, cr_tm=None, md_tm=None, ac_tm=None, company_id=None, copyright='', author=''):
        self.parent_id = parent_id
        self.name = name
        self.mime = mime
        self.size = size
        self.user_id = user_id
        self.cr_tm = cr_tm
        self.md_tm = md_tm
        self.ac_tm = ac_tm

    def __repr__(self):
        return "<File(name='%s', mime=%s', id='%s', parent_id='%s')>" % (
                                self.name, self.mime, self.id, self.parend_id)

    def is_directory(file_id):
        return db.query(File).filter(id=file_id)[0].mime == 'directory'

    def is_cropable(file):
        return File.is_graphics(file)

    def is_graphics(file):
        return re.match('^image/.*', file.mime)

    def list(parent_id=None):
        return list({'size': file.size, 'name': file.name, 'id': file.id,
                                'cropable': True if File.is_cropable(file) else False,
                                'type': 'dir' if file.mime == 'directory' else 'file',
                                'date': str(file.md_tm).split('.')[0]}
                                        for file in db.query(File).filter(File.parent_id == parent_id))

    def createdir(parent_id=None, name=None, company_id=None, copyright='', author=''):
        f = File(parent_id=parent_id, name=name, size=0, company_id=company_id, copyright=copyright, author=author, mime='directory')
        db.add(f)
        db.commit()
        return f.id

    def upload(parent_id=None, file=None, company_id=None, copyright='', author=''):
        f = File(parent_id=parent_id, name=file.filename, company_id=company_id, copyright=copyright, author=author)
        f.content = file.stream.read(-1)
        db.add(f)
        db.commit()
        return f.id

        # file.save(os.path.join(root, filename# ))
        # for tmp_file in os.listdir(root# ):
        #     st = os.stat(root+'/'+filenam# e)
        #     file_db.name = filena# me
        #     file_db.md_tm = time.ctime(os.path.getmtime(root+'/'+filename# ))
        #     file_db.ac_tm = time.ctime(os.path.getctime(root+'/'+filename# ))
        #     file_db.cr_tm = strftime("%Y-%m-%d %H:%M:%S", gmtime(# ))
        #     file_db.size = st[ST_SIZ# E]
        #     if os.path.isfile(root+'/'+tmp_file# ):
        #         file_db.mime = 'fil# e'
        #     els# e:
        #         file_db.mime = 'di# r'

        #
        # binary_out.close# ()
        # if os.path.isfile(root+'/'+filename# ):
        #     os.remove(root+'/'+filenam# e)
        # els# e:
        #     os.removedirs(root+'/'+filenam# e)
        # db_session.add(file_d# b)
        # tr# y:
        #     db_session.commit# ()
        # except PermissionErro# r:
        #     result = {"result":#  {
        #             "success": Fals# e,
        #             "error": "Access denied to remove file# "}
        #        #  }
        #     db_session.rollback#(# )
        #
        # return result
        # return True

class FileContent(Base):
    __tablename__ = 'file_content'
    id = Column(String(36), ForeignKey('file.id'), primary_key=True)
    content = Column(Binary)

    def __init__(self, content=None, id=None):
        self.content = content
        self.id = id
