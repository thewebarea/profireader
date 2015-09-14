import os
from flask import request, render_template, make_response, send_file, g
from flask.ext.login import current_user
# from db_init import db_session
from profapp.models.files import File, FileContent
from .blueprints import filemanager_bp
from io import BytesIO
from .request_wrapers import ok
from functools import wraps
from time import sleep


def parent_folder(func):
    @wraps(func)
    def function_parent_folder(json, *args, **kwargs):
        ret = func(json, *args, **kwargs)
        return ret

    return function_parent_folder


root = os.getcwd() + '/profapp/static/filemanager/tmp'
json_result = {"result": {"success": True, "error": None}}


@filemanager_bp.route('/')
def filemanager():
    # library = {g.user.personal_folder_file_id:
    # {'name': 'My personal files',
    # 'icon': current_user.gravatar(size=18)}}
    library = {
        g.user.personal_folder_file_id: {
            'name': 'My personal files',
            'icon': current_user.profireader_small_avatar_url}}
    for company in g.user.employers:
        library[company.journalist_folder_file_id] = {'name': "%s materisals" % (company.name,), 'icon': ''}
        library[company.corporate_folder_file_id] = {'name': "%s corporate files" % (company.name,), 'icon': ''}

    options = {'mime_allow': '.*', 'mime_deny': '^directory$', 'max_choose': 0, 'on_choose': ''}
    if 'calledby' in request.args:
        if request.args['calledby'] == 'tinymce_file_browse_image':
            options['mime_allow'] = '^image/.*'
            options['max_choose'] = 1
            options['on_choose'] = 'parent.TinyMCE_fileSelected'

    return render_template('filemanager.html', library=library, **options)


@filemanager_bp.route('/list/', methods=['POST'])
@ok
# @parent_folder
def list(json):
    list = File.list(json['params']['folder_id'])
    ancestors = File.ancestors(json['params']['folder_id'])
    return {'list': list, 'ancestors': ancestors}


@filemanager_bp.route('/createdir/', methods=['POST'])
@ok
def createdir(json, parent_id=None):
    return File.createdir(name=request.json['params']['name'],
                          parent_id=request.json['params']['folder_id'])


@filemanager_bp.route('/upload/', methods=['POST'])
@ok
def upload(json):
    sleep(0.1)
    parent_id = request.form['folder_id']
    ret = {}
    for uploaded_file_name in request.files:
        uploaded_file = request.files[uploaded_file_name]
        file = File(parent_id=parent_id, name=uploaded_file.filename,
                mime=uploaded_file.content_type)
        uploaded = file.upload(content=uploaded_file.stream.read(-1))
        ret[uploaded.id] = True
    return ret


# # # #
#
# def upload(result#)# :
#
#     file = request.files['file-1# ']
#     filename = file.filena# me
#     file_db = File# ()
#     file.save(os.path.join(root, filename# ))
#     for tmp_file in os.listdir(root# ):
#         st = os.stat(root+'/'+filenam# e)
#         file_db.name = filena# me
#         file_db.md_tm = time.ctime(
# os.path.getmtime(root+'/'+filename# ))
#         file_db.ac_tm = time.ctime(
# os.path.getctime(root+'/'+filename# ))
#         file_db.cr_tm = strftime("%Y-%m-%d %H:%M:%S", gmtime(# ))
#         file_db.size = st[ST_SIZ# E]
#         if os.path.isfile(root+'/'+tmp_file# ):
#             file_db.mime = 'fil# e'
#         els# e:
#             file_db.mime = 'di# r'
#     binary_out = open(root+'/'+filename, 'rb# ')
#     file_db.content = binary_out.read# ()
#     binary_out.close# ()
#     if os.path.isfile(root+'/'+filename# ):
#         os.remove(root+'/'+filenam# e)
#     els# e:
#         os.removedirs(root+'/'+filenam# e)
#     g.db.add(file_d# b)
#     tr# y:
#         g.db.commit# ()
#     except PermissionErro# r:
#         result = {"result":#  {
#                 "success": Fals# e,
#                 "error": "Access denied to remove file# "}
#            #  }
#         g.db.rollback#(# )
#
#     return result

@filemanager_bp.route('/get/<string:file_id>')
def get(file_id):
    image_query = file_query(file_id, File)
    image_query_content = g.db.query(FileContent).filter_by(
        id=file_id).first()
    response = make_response()
    response.headers['Content-Type'] = image_query.mime
    response.headers['Content-Disposition'] = 'filename=%s' % \
                                              image_query.name
    return send_file(BytesIO(image_query_content.content),
                     mimetype=image_query.mime, as_attachment=False)


def file_query(file_id, table):
    query = g.db.query(table).filter_by(id=file_id).first()
    return query
