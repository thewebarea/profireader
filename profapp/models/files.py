from sqlalchemy import Column, Integer, ForeignKey, String, Binary, UniqueConstraint
import re
from ..constants.TABLE_TYPES import TABLE_TYPES
from utils.db_utils import db
from sqlalchemy.orm import relationship, backref
from flask import url_for, g
from .pr_base import PRBase, Base


class File(Base, PRBase):
    __tablename__ = 'file'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    parent_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('file.id'))
    root_folder_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('file.id'))
    name = Column(TABLE_TYPES['name'], default='', nullable=False)
    mime = Column(String(30), default='text/plain', nullable=False)
    description = Column(TABLE_TYPES['text'], default='', nullable=False)
    copyright = Column(TABLE_TYPES['text'], default='', nullable=False)
    company_id = Column(TABLE_TYPES['id_profireader'],
                        ForeignKey('company.id'),
                        nullable=False)
    article_portal_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('article_portal.id'))
    copyright_author_name = Column(TABLE_TYPES['name'],
                                   default='',
                                   nullable=False)
    ac_count = Column(Integer, default=0, nullable=False)
    size = Column(Integer, default=0, nullable=False)
    author_user_id = Column(TABLE_TYPES['id_profireader'],
                            ForeignKey('user.id'),
                            nullable=False)
    cr_tm = Column(TABLE_TYPES['timestamp'], nullable=False)
    md_tm = Column(TABLE_TYPES['timestamp'], nullable=False)
    ac_tm = Column(TABLE_TYPES['timestamp'], nullable=False)
    youtube_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('youtube_video.id'))

    UniqueConstraint('name', 'parent_id', name='unique_name_in_folder')

    owner = relationship('User',
                         backref=backref('files', lazy='dynamic'),
                         foreign_keys='File.author_user_id',
                         cascade='save-update, delete')

    def __init__(self, parent_id=None, name=None, mime='text/plain', size=0,
                 user_id=None, cr_tm=None, md_tm=None, ac_tm=None,
                 root_folder_id=None, youtube_id = None,
                 company_id=None, author_user_id=None):
        super(File, self).__init__()
        self.parent_id = parent_id
        self.name = name
        self.mime = mime
        self.size = size
        self.user_id = user_id
        self.cr_tm = cr_tm
        self.md_tm = md_tm
        self.root_folder_id = root_folder_id
        self.ac_tm = ac_tm
        self.author_user_id = author_user_id
        self.company_id = company_id
        self.youtube_id = youtube_id

    def __repr__(self):
        return "<File(name='%s', mime=%s', id='%s', parent_id='%s')>" % (
            self.name, self.mime, self.id, self.parent_id)

    @staticmethod
    def is_directory(file_id):
        return db(File, id=file_id)[0].mime == 'directory'

    @staticmethod
    def is_cropable(file):
        return File.is_graphics(file)

    @staticmethod
    def is_graphics(file):
        return re.match('^image/.*', file.mime)

    @staticmethod
    def ancestors(folder_id=None):
        ret = []
        nextf = g.db.query(File).get(folder_id)
        while nextf and len(ret) < 50:
            ret.append(nextf.id)
            nextf = g.db.query(File).get(nextf.parent_id) if nextf.parent_id else None
        return ret[::-1]

    @staticmethod
    def can_paste_in_dir(id_file, id_folder):
        if id_file == id_folder:
            return False
        folder = File.get(id_folder)
        dirs_in_dir = [file for file in db(File, parent_id = id_file, mime='directory')]
        for dir in dirs_in_dir:
            dirs_in_dir.append(dir)
            if dir.parent_id == id_file:
                return False
        return True

    @staticmethod
    def list(parent_id=None, file_manager_called_for = ''):

        default_actions = {}
        # default_actions['choose'] = lambda file: None
        default_actions['download'] = lambda file: None if ((file.mime == 'directory') or (file.mime == 'root')) else True
        actions = {act: default_actions[act] for act in default_actions}
        show = lambda file: True
        actions['rename'] = lambda file: None if file.mime == "root" else True
        actions['remove'] = lambda file: None if file.mime == "root" else True
        actions['copy'] = lambda file: None if file.mime == "root" else True
        actions['paste'] = lambda file: None if file.mime == 'root' else True
        actions['cut'] = lambda file: None if file.mime == "root" else True

        if file_manager_called_for == 'file_browse_image':
            actions['choose'] = lambda file: False if None == re.search('^image/.*', file.mime) else True


            # 'cropable': True if File.is_cropable(file) else False,
        ret = list({'size': file.size, 'name': file.name, 'id': file.id, 'parent_id': file.parent_id,
                                'type': 'dir' if ((file.mime == 'directory') or (file.mime == 'root')) else 'file',
                                'date': str(file.md_tm).split('.')[0],
                    'url': file.url(),
                    'actions': {action:actions[action](file) for action in actions}
                    }
                                        for file in db(File, parent_id = parent_id) if show(file))# we need all records from the table "file"

        return ret

    @staticmethod
    def createdir(parent_id=None, name=None, author_user_id=None,
                  root_folder_id = None,
                  company_id=None, copyright='', author=''):
        f = File(parent_id=parent_id, author_user_id=author_user_id,
                 root_folder_id = root_folder_id,
                 name=name, size=0, company_id=company_id, mime='directory')
        # f = File(parent_id=parent_id, author_user_id=author_user_id, 
        #          name=name, size=0, company_id=company_id, copyright=copyright, mime='directory')
        g.db.add(f)
        g.db.commit()
        return f.id

    @staticmethod
    def create_company_dir(company=None, name=None):
        f = File(parent_id=None, author_user_id=company.author_user_id,
                 name=name, size=0, company_id=company.id, mime='directory')
        g.db.add(f)
        company.company_folder.append(f)
        g.db.commit()
        for x in company.company_folder:
            return x.id

    def upload(self, content):
        file_cont = FileContent(file=self, content=content)
        g.db.add(self, file_cont)
        g.db.commit()
        return self

    def url(self):
        server = re.sub(r'^[^-]*-[^-]*-4([^-]*)-.*$', r'\1', self.id)
        return 'http://file' + server + '.profi.ntaxa.com/' + self.id + '/'

    @staticmethod
    def save_files(files, new_id, attr):
        for file in files:
            attr['parent_id'] = new_id
            file.detach().attr(attr)
            file.save()
        return files

    @staticmethod
    def save_all_in_dir(id, attr, new_id):
        lists = [file for file in db(File, parent_id = id) if file.mime == 'directory']
        files = [file for file in db(File, parent_id = id) if file.mime != 'directory']
        f = File.save_files(files, new_id, attr)
        count_first_list = len(lists)
        c = 1
        c_new = 0
        new_list = []
        for list in lists:
            if c <= count_first_list:
                attr['parent_id'] = new_id
                list.detach().attr(attr)
                list.save()
                new_list.append(list)
            for file in db(File,parent_id = list.id):
                if len(file) > 0 and file.mime == 'directory':
                        lists.append(file)
                        attr['parent_id'] = new_list[c_new].id
                        file.detach().attr(attr)
                        file.save()
                        new_list.append(file)
                elif len(file) > 0 and file.mime != 'directory':
                    file_content = FileContent.get(file.id).detach()
                    attr['parent_id'] = new_list[c_new].id
                    file.detach().attr(attr)
                    file.save()
                    file_content.id = file.id
                    file.file_content = [file_content]
            c_new += 1
            c += 1
        return lists

    @staticmethod
    def save_all(copy_dir_id, attr,files_in_parent):
        del attr['name']
        for fil in files_in_parent:
            if fil.mime == 'directory':
                id_f = {'id':fil.id}
                attr['parent_id'] = copy_dir_id
                copy_directory = fil.detach().attr(attr)
                copy_directory.save()
                save_all_dir = File.save_all_in_dir(id_f['id'],attr,copy_directory.id)
            else:
                file_content = FileContent.get(fil.id).detach()
                attr['parent_id'] = copy_dir_id
                f = fil.detach().attr(attr)
                f.save()
                file_content.id = f.id
                f.file_content = [file_content]
        return files_in_parent
    @staticmethod
    def update_files(files,attr):
        for file in files:
            file.updates(attr)
        return files
    @staticmethod
    def update_all_in_dir(id, attr):
        lists = [file for file in db(File, parent_id = id) if file.mime == 'directory']
        files = [file for file in db(File, parent_id = id) if file.mime != 'directory']
        c = len(lists)
        c_ = 1
        f = File.update_files(files, attr)
        new_list = []
        for list in lists:
            if c_ <= c:
                list.updates(attr)
                new_list.append(list)
            for file in db(File,parent_id = list.id):
                if len(file) > 0 and file.mime == 'directory':
                        lists.append(file)
                        file.updates(attr)
                        new_list.append(file)
                elif len(file) > 0 and file.mime != 'directory':
                    file.updates(attr)
            c_ += 1
        return lists

    @staticmethod
    def update_all(id, attr):
        files_in_parent = [file for file in db(File, parent_id = id)]
        del attr['name']
        del attr['parent_id']
        for fil in files_in_parent:
            if fil.mime == 'directory':
                fil.updates(attr)
                update_all_dir = File.update_all_in_dir(fil.id, attr)
            else:
                fil.updates(attr)
        return files_in_parent

    @staticmethod
    def get_name(oldname):
        ex = File.ext(oldname)
        l = len(ex)
        name = oldname[:-l]
        return  name

    @staticmethod
    def ext(oldname):
        name = oldname[::-1]
        b = name.find('.')
        c = name[0:(b+1):1]
        c = c[::-1]
        return c

    @staticmethod
    def if_copy(name):
        ext = File.ext(name)
        if len(ext)>0 and re.search('\(\d+\)'+ext, name):
            return File.get_name(name)[0:-3]
        elif re.search('\(\d+\)$', name):
            return name[0:-3]
        else:
            name = name if len(ext) == 0 else name[0:-len(ext)]
            return name

    @staticmethod
    def is_name(name, mime, parent_id):
        if [file for file in db(File,parent_id=parent_id, mime=mime, name=name)]:
            return True
        else:
            return False

    @staticmethod
    def get_unique_name(name, mime, parent_id):
        if File.is_name(name, mime, parent_id):
            ext = File.ext(name)
            name = File.if_copy(name)
            list = []
            for n in db(File,parent_id = parent_id, mime=mime):
                if re.match(name+'\(\d+\)'+ext, n.name):
                    pos = (len(n.name) - 2) - len(ext)
                    list.append(int(n.name[pos:pos+1]))
            if list == []:
                return name+'(1)'+ext
            else:
                list.sort()
                index = list[-1] + 1
                return name+'('+str(index)+')'+ext
        else:
            return name

    def rename(self, name):
        if File.is_name(name, self.mime, self.parent_id):
            return False
        else:
            self.updates({'name': name})
            return True

    @staticmethod
    def remove(file_id):
        file = File.get(file_id)
        if file.mime == 'directory':
            b = File.delfile(file)
        else:
            b = File.delfile(FileContent.get(file_id))
        resp = (False if File.get(file_id) else "Success")
        return resp

    def copy_file(self, parent_id, **kwargs):
        id = self.id
        folder = File.get(parent_id)
        root = folder.root_folder_id
        if folder.root_folder_id == None:
            root = folder.id
        attr = {f:kwargs[f] for f in kwargs}
        attr['name'] = File.get_unique_name(self.name, self.mime, parent_id)
        attr['parent_id'] = parent_id
        attr['root_folder_id'] = root
        copy_file = self.detach().attr(attr)
        copy_file.save()
        if self.mime == 'directory':
            files_in_dir = [file for file in db(File,parent_id = id)]
            all_in_dir = File.save_all(copy_file.id, attr,files_in_dir)
        else:
            file_content = FileContent.get(id).detach()
            file_content.id = copy_file.id
            copy_file.file_content = [file_content]
        return copy_file.id

    def move_to(self, parent_id, **kwargs):
        if File.can_paste_in_dir(self.id, parent_id) == False and self.mime == 'directory':
            return False
        if self.parent_id == parent_id:
            return self.id
        folder = File.get(parent_id)
        root = folder.root_folder_id
        if folder.root_folder_id == None:
            root = folder.id
        attr = {f:kwargs[f] for f in kwargs}
        attr['name'] = File.get_unique_name(self.name, self.mime, parent_id)
        attr['parent_id'] = parent_id
        attr['root_folder_id'] = root
        self.updates(attr)
        if self.mime == 'directory':
            b = File.update_all(self.id,attr)
        return self.id

    # def copy_file(self, company_id = None, parent_folder_id = None, article_portal_id = None, root_folder_id = None):
    #     file_content = FileContent.get(self.id).detach()
    #     attr = {}
    #     if company_id:
    #         attr['company_id'] = company_id
    #     if parent_folder_id:
    #         attr['parent_folder_id'] = parent_folder_id
    #     if article_portal_id:
    #         attr['article_portal_id'] = article_portal_id
    #     if root_folder_id:
    #         attr['root_folder_id'] = root_folder_id
    #     new_file = self.detach().attr(attr)
    #     new_file.save()
    #     file_content.id = new_file.id
    #     new_file.file_content = [file_content]
    #     return new_file


class FileContent(Base, PRBase):
    __tablename__ = 'file_content'
    id = Column(TABLE_TYPES['id_profireader'], ForeignKey('file.id'),
                primary_key=True)
    content = Column(Binary, nullable=False)
    file = relationship('File',
                                uselist=False,
                                backref='file_content',
                                cascade='save-update,delete')

    def __init__(self, file=None, content=None):
        self.file = file
        self.content = content

        # file.save(os.path.join(root, filename))
        # for tmp_file in os.listdir(root):
        #     st = os.stat(root+'/'+filename)
        #     file_db.name = filename
        #     file_db.md_tm = time.ctime(os.path.getmtime(root+'/'+filename))
        #     file_db.ac_tm = time.ctime(os.path.getctime(root+'/'+filename))
        #     file_db.cr_tm = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        #     file_db.size = st[ST_SIZE]
        #     if os.path.isfile(root+'/'+tmp_file):
        #         file_db.mime = 'file'
        #     els# e:
        #         file_db.mime = 'dir'

        #
        # binary_out.close# ()
        # if os.path.isfile(root+'/'+filename):
        #     os.remove(root+'/'+filename)
        # else:
        #     os.removedirs(root+'/'+filename)
        # g.db.add(file_db)
        # try:
        #     g.db.commit()
        # except PermissionError:
        #     result = {"result":  {
        #             "success": False,
        #             "error": "Access denied to remove file"}
        #          }
        #     g.db.rollback()
        #
        # return result
        # return True
