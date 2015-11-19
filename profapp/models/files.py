from sqlalchemy import Column, Integer, ForeignKey, String, Binary, UniqueConstraint
import re
from ..constants.TABLE_TYPES import TABLE_TYPES
from utils.db_utils import db
from sqlalchemy.orm import relationship, backref
from flask import g
from .pr_base import PRBase, Base
from ..controllers.errors import VideoAlreadyExistInPlaylist
import json
from config import Config
from urllib import request as req
from flask import session
from urllib.error import HTTPError as response_code
from urllib import parse
from sqlalchemy import desc
from .google import GoogleAuthorize,GoogleToken
import sys

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
    # youtube_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('youtube_video.id'))

    UniqueConstraint('name', 'parent_id', name='unique_name_in_folder')

    owner = relationship('User',
                         backref=backref('files', lazy='dynamic'),
                         foreign_keys='File.author_user_id',
                         cascade='save-update,delete')

    def __init__(self, parent_id=None, name=None, mime='text/plain', size=0,
                 user_id=None, cr_tm=None, md_tm=None, ac_tm=None,
                 root_folder_id=None, youtube_id=None,
                 company_id=None, author_user_id=None, image_croped=None):
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
    def ancestors(folder_id=None, path=False):
        ret = []
        nextf = g.db.query(File).get(folder_id)
        while nextf and len(ret) < 50:
            if path:
                ret.append(nextf.name)
                nextf = g.db.query(File).get(nextf.parent_id) if nextf.parent_id else None
            else:
                ret.append(nextf.id)
                nextf = g.db.query(File).get(nextf.parent_id) if nextf.parent_id else None
        return ret[::-1]

    @staticmethod
    def sort_search(name, files):
        rel_sort = []
        sort = []
        for file in files:
            if re.match(r'^'+name+'.*', file.name.lower()):
                rel_sort.append(file)
            else:
                sort.append(file)
        return rel_sort + sort

    @staticmethod
    def search(name, folder_id, actions, file_manager_called_for=''):
        if name == None:
            return None
        actions['paste'] = lambda file: None
        name = name.lower()
        all_files = File.get_all_in_dir_rev(folder_id)[::-1]
        sort_dirs = []; sort_files = []
        for file in all_files:
            if re.match(r'.*'+name+'.*', file.name.lower()):
                sort_dirs.append(file) if file.mime == 'directory' else sort_files.append(file)
        sort_d = File.sort_search(name, sort_dirs)
        sort_f = File.sort_search(name, sort_files)
        s =  sort_d+sort_f
        ret = list({'size': file.size, 'name': file.name, 'id': file.id, 'parent_id': file.parent_id,
                                'type': File.type(file),
                                'date': str(file.md_tm).split('.')[0],
                    'url': file.url(),
                    'path_to': File.path(file),
                    'author_name': file.copyright_author_name,
                    'description': file.description,
                    'actions': {action: actions[action](file) for action in actions}
                    }
                                        for file in s)
        return ret

    # GETTERS

    @staticmethod
    def list(parent_id=None, file_manager_called_for='', name=None):
        show = lambda file: True

        default_actions = {}
        files = [file for file in db(File, parent_id = parent_id) if show(file)]
        # default_actions['choose'] = lambda file: None
        default_actions['download'] = lambda file: None if ((file.mime == 'directory') or (file.mime == 'root')) else True
        actions = {act: default_actions[act] for act in default_actions}

        actions['remove'] = lambda file: None if file.mime == "root" else True
        actions['copy'] = lambda file: None if file.mime == "root" else True
        actions['paste'] = lambda file: None if file == None else True
        actions['cut'] = lambda file: None if file.mime == "root" else True
        actions['properties'] = lambda file: None if file.mime == "root" else True

        if file_manager_called_for == 'file_browse_image':
            default_actions['choose'] = lambda file: False if None == re.search('^image/.*', file.mime) else True
            actions['choose'] = lambda file: False if None == re.search('^image/.*', file.mime) else True

        search_files = File.search(name, parent_id, actions, file_manager_called_for)
        parent = File.get(parent_id)
        if search_files != None:
            ret = search_files
        else:
            # 'cropable': True if File.is_cropable(file) else False,
            ret = list({'size': file.size, 'name': file.name, 'id': file.id, 'parent_id': file.parent_id,
                                    'type': File.type(file),
                                    'date': str(file.md_tm).split('.')[0],
                        'url': file.url(),
                        'path_to': File.path(file),
                        'author_name': file.copyright_author_name,
                        'description': file.description,
                        'actions': {action: actions[action](file) for action in actions},
                        }
                                            for file in db(File, parent_id = parent_id) if show(file))# we need all records from the table "file"
            ret.append({ 'id': parent.id, 'parent_id': parent.parent_id,
                                    'type': 'parent',
                                    'date': str(parent.md_tm).split('.')[0],
                        'url': parent.url(),
                        'author_name': parent.copyright_author_name,
                        'description': parent.description,
                        'actions': {action: actions[action](parent) for action in actions},
                        })

        return ret

    def type(self):
        if self.mime == 'root' or self.mime == 'directory':
            return 'dir'
        elif self.mime == 'video/*':
            return 'file_video'
        else:
            return 'file'

    def path(self):
        parents = File.ancestors(self.parent_id, True)
        del parents[0]
        path = '/'
        for dir in parents:
            path += dir+'/'
        path += self.name
        return path

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
                if re.match(r'^'+name+'\(\d+\)'+''+ext+'', n.name):
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

    def set_properties(self, add_all, **kwargs):
        if self == None:
            return False
        attr = {f:kwargs[f] for f in kwargs}
        check = File.is_name(attr['name'], self.mime, self.parent_id) if attr['name'] != 'None' else True
        if attr['name'] == 'None':
            del attr['name']
        self.updates(attr)
        if add_all:
            if 'name' in attr.keys():
                del attr['name']
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
                elif f.mime == 'video/*':
                    YoutubeVideo.delfile(YoutubeVideo.get(f.id))
                else:
                    FileContent.delfile(FileContent.get(f.id))
            File.delfile(file)
        elif file.mime == 'video/*':
            YoutubeVideo.delfile(YoutubeVideo.get(file.id))
        else:
            FileContent.delfile(FileContent.get(file_id))
        resp = (False if File.get(file_id) else "Success")
        return resp

    @staticmethod
    def save_files(files, new_id, attr):
        for file in files:
            if file.mime == 'video/*':
                youtube_video = YoutubeVideo.get(file.youtube_id).detach()
                attr['parent_id'] = new_id
                file.detach().attr(attr)
                file.save()
                file.youtube_video = youtube_video
            else:
                file_content = FileContent.get(file.id).detach()
                attr['parent_id'] = new_id
                file.detach().attr(attr)
                file.save()
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
                File.save_files(files, dir.id, attr)
            else:
                old_list.append(dir.id)
                files = [file for file in db(File, parent_id=dir.id) if file.mime != 'directory']
                parent = File.get(dir.parent_id)
                index = File.get_index(parent, old_list)
                attr['parent_id'] = new_list[index].id
                dir.detach().attr(attr)
                dir.save()
                new_list.append(dir)
                File.save_files(files, dir.id, attr)
        return old_list, new_list

    @staticmethod
    def upload(name, data, parent, root, content):
        if data.get('chunkNumber') == '0':
            file = File(parent_id=parent,
                        root_folder_id=root,
                        name=name,
                        mime=data.get('ftype'),
                        size=data.get('totalSize')
                        ).save()
            file_cont = FileContent(file=file, content=content)
            g.db.add(file, file_cont)
            g.db.commit()
            session['f_id'] = file.id
            return file.id
        else:
            id = session['f_id']
            file_cont = FileContent.get(id)
            cont = bytes(file_cont.content)
            c = cont + bytes(content)
            file_cont.updates({'content': c})
            return id

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
        File.update_files(files, attr)
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
                File.update_all_in_dir(fil.id, attr)
            else:
                fil.updates(attr)
        return files_in_parent

    def copy_file(self, parent_id, **kwargs):
        folder = File.get(parent_id)
        if self == None or folder == None:
            return False
        id = self.id
        # youtube_id = self.youtube_id
        root = folder.root_folder_id
        if folder.root_folder_id == None:
            root = folder.id
        attr = {f: kwargs[f] for f in kwargs}
        attr['name'] = File.get_unique_name(self.name, self.mime, parent_id)
        attr['parent_id'] = parent_id
        attr['root_folder_id'] = root
        copy_file = self.detach().attr(attr)
        copy_file.save()
        if self.mime == 'directory':
            File.save_all(id, attr, copy_file.id)
        elif self.mime == 'video/*':
            youtube_video = YoutubeVideo.get(youtube_id).detach()
            copy_file.youtube_video = youtube_video
        else:
            file_content = FileContent.get(id).detach()
            copy_file.file_content = file_content

        return copy_file

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
            File.update_all(self.id, attr)
        return self.id


class FileContent(Base, PRBase):
    __tablename__ = 'file_content'
    id = Column(TABLE_TYPES['id_profireader'], ForeignKey('file.id'),
                primary_key=True)
    content = Column(Binary, nullable=False)
    file = relationship('File',
                                uselist=False,
                                backref=backref('file_content', uselist=False),
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


class YoutubeApi(GoogleAuthorize):
    """ Use this class for upload videos, get videos, create channels.
        To udpload videos body should be dict like this:
        {
         "title": "My video title",
         "description": "This is a description of my video",
         "tags": ["profireader", "video", "more keywords"],
         "categoryId": 22
         "status": "public"
         }
         Video will uploaded via chunks .You should, pass chunk info (dict) to constructor like:
         chunk_size = 10240 (in bytes) must be multiple 256kb, chunk_number = 0-n (from zero),
         total_size = 1000000
         Requirements : parts = 'snippet' .Pass to this what would you like to return from
          youtube server. (id, snippet, status, contentDetails, fileDetails, player,
          processingDetails, recordingDetails, statistics, suggestions, topicDetails)"""

    def __init__(self, parts=None, video_file=None, body_dict=None, chunk_info=None,
                 company_id=None, root_folder_id=None, parent_folder_id=None):
        super(YoutubeApi, self).__init__()
        self.video_file = video_file
        self.body_dict = body_dict
        self.chunk_info = chunk_info
        self.resumable = True if self.chunk_info else False
        self.parts = parts
        self.start_session = Config.YOUTUBE_API['UPLOAD']['SEND_URI']
        self.company_id = company_id
        self.root_folder_id = root_folder_id
        self.parent_folder_id = parent_folder_id

    def make_body_for_start_upload(self):
        """ make body to create request. category_id default 22, status default 'public'. """

        body = dict(snippet=dict(
                    title=self.body_dict.get('title') or '',
                    description=self.body_dict.get('description') or '',
                    tags=self.body_dict.get('tags'),
                    categoryId=self.body_dict.get('category_id') or 22),
                    status=dict(
                    privacyStatus=self.body_dict.get('status') or 'public'))
        return body

    def make_headers_for_start_upload(self, content_length):
        """ This method make headers for preupload request to get url for upload binary data.
         content_length should be body length in bytes. First step to start upload """
        authorization = GoogleToken.get_credentials_from_db().access_token
        session['authorization'] = authorization
        headers = {'authorization': 'Bearer {0}'.format(authorization),
                   'content-type': 'application/json; charset=utf-8',
                   'content-length': content_length,
                   'x-upload-content-length': self.chunk_info.get('total_size'),
                   'x-upload-content-type': 'application/octet-stream'}

        return headers

    def make_encoded_url_for_upload(self, body_keys, **kwargs):
        """ This method make values of header url encoded.
         body_keys are values which you want to return from youtube server """
        values = parse.urlencode(dict(uploadType='resumable', part=",".join(body_keys)))
        url_encoded = self.start_session % values
        return url_encoded

    def set_youtube_upload_service_url_to_session(self):

        """ This method add to flask session video_id and url from youtube server and url for upload
         videos. If raise except - bad credentials """
        body = self.make_body_for_start_upload()
        url = self.make_encoded_url_for_upload(body.keys())
        body = json.dumps(body).encode('utf8')
        headers = self.make_headers_for_start_upload(sys.getsizeof(body))
        r = req.Request(url=url, headers=headers,  method='POST')
        response = req.urlopen(r, data=body)
        session['video_id'] = response.headers.get('X-Goog-Correlation-Id')
        session['url'] = response.headers.get('Location')

    def make_headers_for_upload(self):
        """ This method make headers for upload videos. Second  step to start upload """
        headers = {'authorization': 'Bearer {0}'.format(session.get('access_token')),
                   'content-type': 'application/octet-stream',
                   'content-length': self.chunk_info.get('chunk_size'),
                   'content-range': 'bytes 0-{0}/{1}'.format(
                       self.chunk_info.get('chunk_size')-1, self.chunk_info.get('total_size'))}
        return headers

    def make_headers_for_resumable_upload(self):
        """ This method make headers for resumable upload videos. Thirst step to start upload """
        video = db(YoutubeVideo, id=session['id']).one()
        last_byte = self.chunk_info.get('chunk_size') + video.size - 1
        last_byte = self.chunk_info.get('total_size') - 1 if (self.chunk_info.get(
            'chunk_size') + video.size - 1) > self.chunk_info.get('total_size') else last_byte
        headers = {'authorization': 'Bearer {0}'.format(video.authorization),
                   'content-type': 'application/octet-stream',
                   'content-length': self.chunk_info.get('total_size')-video.size - 1,
                   'content-range': 'bytes {0}-{1}/{2}'.format(video.size,
                                                               last_byte,
                                                               self.chunk_info.get('total_size'))}
        return headers

    def check_upload_status(self):
        """ You can use this method to check upload status. If except you will get error
        code from youtube server """
        headers = {'authorization': 'Bearer {0}'.format(session.get('access_token')),
                   'content-range': 'bytes */{0}'.format(self.chunk_info.get('total_size')),
                   'content-length': 0}
        r = req.Request(url=session['url'], headers=headers,  method='PUT')
        try:
            response = req.urlopen(r)
            return response
        except response_code as e:
            print(e.code)

    def upload(self):

        """ Use this method for upload videos. If video_id you can get from session['video_id'].
          If except error 308 - video has not yet been uploaded, call resumable_upload().
          If chunk > 0 run resumable_upload method. If video was uploaded return 200 or 201 code:
          success """
        chunk_number = self.chunk_info.get('chunk_number')
        if not chunk_number:
            self.set_youtube_upload_service_url_to_session()
        headers = self.make_headers_for_upload()
        playlist = YoutubePlaylist.get_not_full_company_playlist(self.company_id)
        try:
            if not chunk_number:
                r = req.Request(url=session['url'], headers=headers, method='PUT')
                response = req.urlopen(r, data=self.video_file,)
                if response.code == 200 or response.code == 201:
                    name = File.get_unique_name(self.body_dict['title'], 'video/*', self.parent_folder_id)
                    file = File(parent_id=self.parent_folder_id,
                                root_folder_id=self.root_folder_id,
                                name=name,
                                size=self.chunk_info.get('total_size'),
                                mime='video/*')
                    youtube = YoutubeVideo(file=file, authorization=session['authorization'].split(' ')[-1],
                                           size=self.chunk_info.get('total_size'),
                                           user_id=g.user_dict['id'],
                                           video_id=session['video_id'],
                                           status='uploaded',
                                           playlist=playlist)
                    g.db.add(file, youtube)
                    g.db.commit()
                    session['id'] = file.id
                    youtube.put_video_in_playlist()
                    return 'success'
        except response_code as e:
            if e.code == 308 and not chunk_number:
                name = File.get_unique_name(self.body_dict['title'], 'video/*', self.parent_folder_id)
                file = File(parent_id=self.parent_folder_id,
                            root_folder_id=self.root_folder_id,
                            name=name,
                            size=self.chunk_info.get('total_size'),
                            mime='video/*')
                youtube = YoutubeVideo(file=file, authorization=session['authorization'].split(' ')[-1],
                                       size=int(e.headers.get('Range').split('-')[-1])+1,
                                       user_id=g.user_dict['id'],
                                       video_id=session['video_id'],
                                       playlist=playlist
                                       )
                g.db.add(file, youtube)
                g.db.commit()
                session['id'] = file.id
                youtube.put_video_in_playlist()
                return 'uploading'
        if chunk_number:
            return self.resumable_upload()

    def resumable_upload(self):
        """ This method is useful when you upload video via chunks. Pass video_id from db to flask
        session. """
        headers = self.make_headers_for_resumable_upload()
        r = req.Request(url=session['url'], headers=headers, method='PUT')

        try:
            response = req.urlopen(r, data=self.video_file)
            if response.code == 200 or response.code == 201:
                video = db(YoutubeVideo, id=session['id'])
                video.update({'size': self.chunk_info.get('total_size'), 'status': 'uploaded'})
                return 'success'
        except response_code as e:
            if e.code == 308:
                db(YoutubeVideo, id=session['id']).update(
                    {'size': int(e.headers.get('Range').split('-')[-1])+1})
            return 'uploading'


class YoutubeVideo(Base, PRBase):
    """ This class make models for youtube videos.
     status video should be 'uploading' or 'uploaded' """
    __tablename__ = 'youtube_video'
    # id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
    id = Column(TABLE_TYPES['id_profireader'], ForeignKey('file.id'),
                primary_key=True)
    video_id = Column(TABLE_TYPES['short_text'])
    title = Column(TABLE_TYPES['name'], default='Title')
    authorization = Column(TABLE_TYPES['token'])
    size = Column(TABLE_TYPES['bigint'])
    user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'))
    status = Column(TABLE_TYPES['string_30'], default='uploading')
    playlist_id = Column(TABLE_TYPES['short_text'], ForeignKey('youtube_playlist.playlist_id'),
                         nullable=False)
    playlist = relationship('YoutubePlaylist', uselist=False)
    file = relationship('File',
                                uselist=False,
                                backref=backref('youtube_video', uselist=False),
                                cascade='save-update,delete')

    def __init__(self, file=None, title='Title', authorization=None, size=None, user_id=None, video_id=None,
                 status='uploading', playlist_id=None, playlist=None):
        super(YoutubeVideo, self).__init__()
        self.file = file
        self.title = title
        self.authorization = authorization
        self.size = size
        self.user_id = user_id
        self.video_id = video_id
        self.status = status
        self.playlist_id = playlist_id
        self.playlist = playlist

    def put_video_in_playlist(self):

        """ This method put video to playlist and return response """
        body = self.make_body_to_put_video_in_playlist()
        url = self.make_encoded_url_to_put_video_in_playlist()
        body = json.dumps(body).encode('utf8')
        headers = self.make_headers_to_put_video_in_playlist(sys.getsizeof(body))
        try:
            r = req.Request(url=url, headers=headers,  method='POST')
            response = req.urlopen(r, data=body)
            response_str_from_bytes = response.readall().decode('utf-8')
            fields = json.loads(response_str_from_bytes)
            return fields
        except response_code as e:
            if e.reason == 'duplicate':
                raise VideoAlreadyExistInPlaylist({'message': 'Video already exist in playlist'})
            elif e.reason == 'forbidden':
                self.playlist.add_video_to_cloned_playlist_with_new_name(self)

    def make_encoded_url_to_put_video_in_playlist(self):
        """ This method make values of header url encoded.
         part are values which you want to send to youtube server """
        values = parse.urlencode(dict(part='snippet'))
        url_encoded = Config.YOUTUBE_API['PLAYLIST_ITEMS']['SEND_URI'] % values
        return url_encoded

    def make_body_to_put_video_in_playlist(self):
        """ make body """
        body = dict(snippet=dict(playlistId=self.playlist_id,
                                 resourceId=dict(videoId=self.video_id, kind='youtube#video')))
        return body

    def make_headers_to_put_video_in_playlist(self, content_length):
        """ This method make headers .
         content_length should be body length in bytes. """
        authorization = GoogleToken.get_credentials_from_db().access_token
        headers = {'authorization': 'Bearer {0}'.format(authorization),
                   'content-type': 'application/json; charset=utf-8',
                   'content-length': content_length}
        return headers


class YoutubePlaylist(Base, PRBase):
    __tablename__ = 'youtube_playlist'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
    playlist_id = Column(TABLE_TYPES['short_text'], nullable=False, unique=True)
    name = Column(TABLE_TYPES['short_text'], unique=True)
    company_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company.id'))
    company_owner = relationship('Company', uselist=False)
    md_tm = Column(TABLE_TYPES['timestamp'])

    def __init__(self, name=None, company_id=None, company_owner=None):
        super(YoutubePlaylist, self).__init__()
        self.name = name
        self.company_id = company_id
        self.company_owner = company_owner
        self.playlist_id = self.create_new_playlist().get('id')
        self.save()

    def create_new_playlist(self):

        """ This method create playlist and return response """
        body = self.make_body_to_get_playlist_url()
        url = self.make_encoded_url_for_playlists()
        body = json.dumps(body).encode('utf8')
        headers = self.make_headers_to_get_playlists(sys.getsizeof(body))
        r = req.Request(url=url, headers=headers,  method='POST')
        response = req.urlopen(r, data=body)
        response_str_from_bytes = response.readall().decode('utf-8')
        fields = json.loads(response_str_from_bytes)
        return fields

    def make_body_to_get_playlist_url(self):
        """ make body to create playlist """

        body = dict(snippet=dict(title=self.name),
                    status=dict(privacyStatus='public'))
        return body

    def make_encoded_url_for_playlists(self):
        """ This method make values of header url encoded.
         part are values which you want to send to youtube server """
        values = parse.urlencode(dict(part='snippet,status'))
        url_encoded = Config.YOUTUBE_API['CREATE_PLAYLIST']['SEND_URI'] % values
        return url_encoded

    def make_headers_to_get_playlists(self, content_length):
        """ This method make headers for create playlist.
         content_length should be body length in bytes. """
        authorization = GoogleToken.get_credentials_from_db().access_token
        session['authorization'] = authorization
        headers = {'authorization': 'Bearer {0}'.format(authorization),
                   'content-type': 'application/json; charset=utf-8',
                   'content-length': content_length}
        return headers

    @staticmethod
    def get_not_full_company_playlist(company_id):
        """ Return not full company playlist. Pass company id. """
        playlist = db(YoutubePlaylist, company_id=company_id).order_by(
            desc(YoutubePlaylist.md_tm)).first()
        return playlist

    def add_video_to_cloned_playlist_with_new_name(self, video):
        # TODO DOES NOT TESTED YET !!! IF DOES NOT WORK ASK VIKTOR
        playlist = self.detach()
        playlist.name = self.name + '*'
        playlist.save()
        video.playlist = playlist
        return playlist
