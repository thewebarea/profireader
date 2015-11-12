from sqlalchemy import Column, Integer, ForeignKey, String, Binary, UniqueConstraint
import re
from ..constants.TABLE_TYPES import TABLE_TYPES
from utils.db_utils import db
from sqlalchemy.orm import relationship, backref
from flask import url_for, g
from .pr_base import PRBase, Base
from flask import make_response


# TODO: (AA to AA): change article_portal_id to article_portal_division_id in table
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
    article_portal_division_id = Column(TABLE_TYPES['id_profireader'],
                                        ForeignKey('article_portal_division.id'))
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
    file_content = relationship('FileContent', uselist=False)

    UniqueConstraint('name', 'parent_id', name='unique_name_in_folder')

    owner = relationship('User',
                         backref=backref('files', lazy='dynamic'),
                         foreign_keys='File.author_user_id')

    def __init__(self, parent_id=None, name=None, mime='text/plain', size=0,
                 user_id=None, cr_tm=None, md_tm=None, ac_tm=None,
                 root_folder_id=None, youtube_id=None,
                 company_id=None, author_user_id=None, image_croped=None, file_content=None):
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
        self.image_croped = image_croped
        self.file_content = file_content

    def __repr__(self):
        return "<File(name='%s', mime=%s', id='%s', parent_id='%s')>" % (
            self.name, self.mime, self.id, self.parent_id)

    # CHECKING

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
    def can_paste_in_dir(id_file, id_folder):
        if id_file == id_folder:
            return False
        folder = File.get(id_folder)
        dirs_in_dir = [file for file in db(File, parent_id = id_file, mime='directory')]
        for dir in dirs_in_dir:
            for f in db(File, parent_id = dir.id, mime='directory'):
                dirs_in_dir.append(f)
            if dir.id == id_folder:
                return False
        return True

    @staticmethod
    def ancestors(folder_id=None):
        ret = []
        nextf = g.db.query(File).get(folder_id)
        while nextf and len(ret) < 50:
            ret.append(nextf.id)
            nextf = g.db.query(File).get(nextf.parent_id) if nextf.parent_id else None
        return ret[::-1]

    # GETTERS

    @staticmethod
    def list(parent_id=None, file_manager_called_for=''):

        default_actions = {}
        # default_actions['choose'] = lambda file: None
        default_actions['download'] = lambda file: None if ((file.mime == 'directory') or (file.mime == 'root')) else True
        actions = {act: default_actions[act] for act in default_actions}
        show = lambda file: True
        actions['remove'] = lambda file: None if file.mime == "root" else True
        actions['copy'] = lambda file: None if file.mime == "root" else True
        actions['paste'] = lambda file: None if file == None else True
        actions['cut'] = lambda file: None if file.mime == "root" else True
        actions['properties'] = lambda file: None if file.mime == "root" else True

        parent = File.get(parent_id)

        if file_manager_called_for == 'file_browse_image':
            actions['choose'] = lambda file: False if None == re.search('^image/.*', file.mime) else True


            # 'cropable': True if File.is_cropable(file) else False,
        ret = list({'size': file.size, 'name': file.name, 'id': file.id, 'parent_id': file.parent_id,
                                'type': 'dir' if ((file.mime == 'directory') or (file.mime == 'root')) else 'file',
                                'date': str(file.md_tm).split('.')[0],
                    'url': file.url(),
                    'author_name': file.copyright_author_name,
                    'description': file.description,
                    'actions': {action: actions[action](file) for action in actions},
                    }
                                        for file in db(File, parent_id = parent_id) if show(file))# we need all records from the table "file"
        ret.append({'name': parent.name, 'id': parent.id, 'parent_id': parent.parent_id,
                                'type': 'parent',
                                'date': str(parent.md_tm).split('.')[0],
                    'url': parent.url(),
                    'author_name': parent.copyright_author_name,
                    'description': parent.description,
                    'actions': {action: actions[action](parent) for action in actions},
                    })

        return ret


    def url(self):
        server = re.sub(r'^[^-]*-[^-]*-4([^-]*)-.*$', r'\1', self.id)
        return 'http://file' + server + '.profireader.com/' + self.id + '/'

    @staticmethod
    def get_index(file, lists):
        i = 0
        for f in lists:
            if file.id == f:
                return i
            i += 1
        return False

    @staticmethod
    def get_all_in_dir_rev(id):
        files_in_parent = [file for file in db(File, parent_id=id)]
        for file in files_in_parent:
            if file.mime == 'directory':
                for fil in db(File, parent_id=file.id):
                    files_in_parent.append(fil)
        files_in_parent = files_in_parent[::-1]
        return files_in_parent

    @staticmethod
    def get_all_dir(f_id, copy_id=None):
        files_in_parent = [file for file in db(File, parent_id=f_id) if file.mime == 'directory' and file.id != copy_id]
        for file in files_in_parent:
            if file.mime == 'directory':
                for fil in db(File, parent_id=file.id, mime='directory'):
                    files_in_parent.append(fil) if fil.id != copy_id else None
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
    def get_unique_name(name, mime, parent_id):
        if File.is_name(name, mime, parent_id):
            ext = File.ext(name)
            name = File.if_copy(name)
            list = []
            for n in db(File,parent_id = parent_id, mime=mime):
                if re.match(r'name'+'\(\d+\)'+'ext', n.name):
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

    # ACTIONS

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

    @staticmethod
    def search(serch_text, folder_id):
        # files = []
        # prop = []
        # name = name.lower()
        # prog = re.compile(r'.*'+name+'.*')
        # for root in roots:
        #     for file in db(File, root_folder_id=root):
        #         if re.match(r'^'+name+'.*',file.name.lower()):
        #             prop.append(file)
        #         elif re.match(r'.*'+name+'.*',file.name.lower()):
        #             files.append(file)
        # prop.extend(files)
        sub_query = File.get_all_in_dir_rev(folder_id)
        # if search_text:
        #     sub_query = sub_query.filter(ArticleCompany.title.ilike("%" + search_text + "%"))
        # if kwargs.get('portal_id') or kwargs.get('status'):
        #     sub_query = sub_query.filter(db(ArticlePortal, article_company_id=ArticleCompany.id,
        #                                     **kwargs).exists())

        return sub_query


    def set_properties(self, add_all,**kwargs):
        if self == None:
            return False
        attr = {f:kwargs[f] for f in kwargs if kwargs[f] != ''}
        check = File.is_name(attr['name'], self.mime, self.parent_id) if attr['name'] != 'None' else True
        if attr['name'] == 'None':
            del attr['name']
        self.updates(attr)
        if add_all:
            files = File.get_all_in_dir_rev(self.id)
            for file in files:
                file.updates(attr)
        return check

    def rename(self, name):
        if self == None:
            return False
        if File.is_name(name, self.mime, self.parent_id):
            return False
        else:
            self.updates({'name': name})
            return True

    @staticmethod
    def remove(file_id):
        file = File.get(file_id)
        if file == None:
            return False
        if file.mime == 'directory':
            list = File.get_all_in_dir_rev(file_id)
            for f in list:
                if f.mime == 'directory':
                    File.delfile(f)
                else:
                    File.delfile(FileContent.get(f.id))
            b = File.delfile(file)
        else:
            b = File.delfile(FileContent.get(file_id))
        resp = (False if File.get(file_id) else "Success")
        return resp

    @staticmethod
    def save_files(files, new_id, attr):
        for file in files:
            file_content = FileContent.get(file.id).detach()
            attr['parent_id'] = new_id
            file.detach().attr(attr)
            file.save()
            file_content.id = file.id
            file.file_content = file_content
        return files

    @staticmethod
    def save_all(id_f, attr, new_id):
        del attr['name']
        lists = File.get_all_dir(id_f, new_id)
        files = [file for file in db(File, parent_id=id_f) if file.mime != 'directory']
        f = File.save_files(files, new_id, attr)
        new_list = []
        old_list = []
        for dir in lists:
            if dir.parent_id == id_f:
                old_list.append(dir.id)
                attr['parent_id'] = new_id
                files = [file for file in db(File, parent_id=dir.id) if file.mime != 'directory']
                dir.detach().attr(attr)
                dir.save()
                new_list.append(dir)
                f = File.save_files(files, dir.id, attr)
            else:
                old_list.append(dir.id)
                files = [file for file in db(File, parent_id=dir.id) if file.mime != 'directory']
                parent = File.get(dir.parent_id)
                index = File.get_index(parent, old_list)
                attr['parent_id'] = new_list[index].id
                dir.detach().attr(attr)
                dir.save()
                new_list.append(dir)
                f = File.save_files(files, dir.id, attr)
        return old_list, new_list

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
                if file.mime == 'directory':
                        lists.append(file)
                        file.updates(attr)
                        new_list.append(file)
                elif file.mime != 'directory':
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



    def copy_file(self, parent_id, **kwargs):
        folder = File.get(parent_id)
        if self == None or folder == None:
            return False
        id = self.id
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
            all_in_dir = File.save_all(id, attr, copy_file.id)
        else:
            file_content = FileContent.get(id).detach()
            # file_content.id = copy_file.id
            copy_file.file_content = file_content

        return copy_file.id

    def move_to(self, parent_id, **kwargs):
        folder = File.get(parent_id)
        if self == None or folder == None:
            return False
        if File.can_paste_in_dir(self.id, parent_id) == False and self.mime == 'directory':
            return False
        if self.parent_id == parent_id:
            return self.id
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


class FileContent(Base, PRBase):
    __tablename__ = 'file_content'
    id = Column(TABLE_TYPES['id_profireader'], ForeignKey('file.id'),
                primary_key=True)
    content = Column(Binary, nullable=False)
    file = relationship('File', uselist=False)

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


class ImageCroped(Base, PRBase):
    __tablename__ = 'image_croped'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False, unique=True, primary_key=True)
    original_image_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('file.id'), nullable=False)
    croped_image_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('file.id'), nullable=False)
    x = Column(TABLE_TYPES['int'], nullable=False)
    y = Column(TABLE_TYPES['int'], nullable=False)
    width = Column(TABLE_TYPES['int'], nullable=False)
    height = Column(TABLE_TYPES['int'], nullable=False)
    rotate = Column(TABLE_TYPES['int'], nullable=False)

    def __init__(self, original_image_id=None, x=None, y=None, width=None, height=None, rotate=None,
                 croped_image_id=None):
        super(ImageCroped, self).__init__()
        self.original_image_id = original_image_id
        self.croped_image_id = croped_image_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotate = rotate

    def get_client_side_dict(self, fields='x,y,width,height,rotate'):
        """This method make dictionary from portal object with fields have written above"""
        return self.to_dict(fields)

    @staticmethod
    def get_coordinates_and_original_img(croped_image_id):
        coor_img = db(ImageCroped, croped_image_id=croped_image_id).one()
        return coor_img.original_image_id, {'coordinates': coor_img.get_client_side_dict()}
