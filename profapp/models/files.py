from _ast import In
from sqlalchemy import Column, Integer, ForeignKey, String, Binary, Float, TIMESTAMP, UniqueConstraint
from db_init import Base, db_session
import re
from ..constants.TABLE_TYPES import TABLE_TYPES
def db(*args, **kwargs):
    return db_session.query(args[0]).filter_by(**kwargs)

class File(Base):
    __tablename__ = 'file'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    parent_id = Column(String(36), ForeignKey('file.id'))
    name = Column(TABLE_TYPES['name'], default='', nullable=False)
    mime = Column(String(30), default='text/plain', nullable=False)
    description = Column(TABLE_TYPES['text'], default='', nullable=False)
    copyright = Column(TABLE_TYPES['text'], default='', nullable=False)
    company_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company.id'), nullable=False)
    author_name = Column(TABLE_TYPES['name'], default='', nullable=False)
    ac_count = Column(Integer, default=0, nullable=False)
    size = Column(Integer, default=0, nullable=False)
    author_user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'), nullable=False)
    cr_tm = Column(TABLE_TYPES['timestamp'], nullable=False)
    md_tm = Column(TABLE_TYPES['timestamp'], nullable=False)
    ac_tm = Column(TABLE_TYPES['timestamp'], nullable=False)

    UniqueConstraint('name', 'parent_id', name='inique_name_in_folder')

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
        return db(File, id=file_id)[0].mime == 'directory'

    def is_cropable(file):
        return File.is_graphics(file)

    def is_graphics(file):
        return re.match('^image/.*', file.mime)

    def list(parent_id=None):
        return list({'size': file.size, 'name': file.name, 'id': file.id,
                                'cropable': True if File.is_cropable(file) else False,
                                'type': 'dir' if file.mime == 'directory' else 'file',
                                'date': str(file.md_tm).split('.')[0]}
                                        for file in db(File, File.parent_id == parent_id))

    def createdir(parent_id=None, name=None, company_id=None, copyright='', author=''):
        f = File(parent_id=parent_id, name=name, size=0, company_id=company_id, copyright=copyright, author=author, mime='directory')
        db_session.add(f)
        db_session.commit()
        return f.id

    def upload(parent_id=None, file=None, company_id=None, copyright='', author=''):
        f = File(parent_id=parent_id, name=file.filename, company_id=company_id, copyright=copyright, author=author)
        f.content = file.stream.read(-1)
        db_session.add(f)
        db_session.commit()
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
    id = Column(TABLE_TYPES['id_profireader'], ForeignKey('file.id'), primary_key=True)
    content = Column(Binary)

    def __init__(self, content=None, id=None):
        self.content = content
        self.id = id
