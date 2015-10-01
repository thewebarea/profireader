import os
from flask import request, render_template, make_response, send_file, g
from flask.ext.login import current_user
# from db_init import db_session
from profapp.models.files import File, FileContent
from .blueprints import filemanager_bp
from .request_wrapers import ok
from functools import wraps
from time import sleep
from flask import jsonify
import json as jsonmodule
# from ..models.youtube import YoutubeApi


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
    library = {}
    for user_company in g.user.employer_assoc:

# TODO VK by OZ: we need function that get all emploees with specific right
# Company.get_emploees('can_read', status = 'active')
# Company.get_emploees(['can_read', 'can_write'], status = ['active','banned'])
# similar function User.get_emploers ...

        if user_company.status == 'active' and 'upload_files' in g.user.user_rights_in_company(user_company.company_id):
            library[user_company.employer.journalist_folder_file_id] = {'name': "%s files" % (user_company.employer.name,), 'icon': ''}
            # library[user_company.employer.corporate_folder_file_id] = {'name': "%s corporate files" % (user_company.employer.name,), 'icon': ''}

    file_manager_called_for = request.args['file_manager_called_for'] if 'file_manager_called_for' in request.args else ''
    file_manager_on_action = jsonmodule.loads(request.args['file_manager_on_action']) if 'file_manager_on_action' in request.args else {}

    return render_template('filemanager.html', library=library,
                           file_manager_called_for=file_manager_called_for,
                           file_manager_on_action = file_manager_on_action)


@filemanager_bp.route('/list/', methods=['POST'])
@ok
# @parent_folder
def list(json):
    list = File.list(json['params']['folder_id'], json['params']['file_manager_called_for'])
    ancestors = File.ancestors(json['params']['folder_id'])
    return {'list': list, 'ancestors': ancestors}


@filemanager_bp.route('/createdir/', methods=['POST'])
@ok
def createdir(json, parent_id=None):
    return File.createdir(name=request.json['params']['name'],
                          root_folder_id=request.json['params']['root_id'],
                          parent_id=request.json['params']['folder_id'])


@filemanager_bp.route('/upload/', methods=['POST'])
@ok
def upload(json):
    sleep(0.1)
    parent_id = request.form['folder_id']
    root_id = request.form['root_id']
    ret = {}
    for uploaded_file_name in request.files:
        uploaded_file = request.files[uploaded_file_name]
        file = File(parent_id=parent_id,
                    root_folder_id=root_id,
                    name=uploaded_file.filename,
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
# from ..models.youtube import YoutubeApi

@filemanager_bp.route('/uploader/', methods=['GET'])
def uploader():
    # youtube = YoutubeApi()
    # youtube.p()
    return render_template('file_uploader.html')


@filemanager_bp.route('/send/', methods=['POST'])
def send():
    print(request.headers)

    return jsonify({'result': {'size': 0}})


@filemanager_bp.route('/resumeopload/', methods=['GET'])
def resumeopload():

    return jsonify({'size': 0})
