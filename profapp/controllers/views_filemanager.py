import os
import time
from time import gmtime, strftime
from stat import ST_SIZE
from flask import jsonify, request, render_template
from db_init import db_session
from profapp.models.files import File
from .blueprints import filemanager_bp, static_bp
from .request_wrapers import json, parent_folder

root = os.getcwd()+'/profapp/static/filemanager/tmp'
json_result = {"result": {"success": True, "error": None}}


@filemanager_bp.route('/', methods=['GET', 'POST'])
def filemanager():
    return render_template('filemanager.html')


@filemanager_bp.route('/list/', methods=['POST'])
@json
@parent_folder
def list(parent_id=None):
    return File.list(parent_id = parent_id)

@filemanager_bp.route('/createdir/', methods=['POST'])
@json
@parent_folder
def createdir(parent_id=None):
    return File.createdir(name = request.json['params']['name'],  parent_id = parent_id)

@filemanager_bp.route('/upload/', methods=['POST'])
@json
def upload():
    parent_id = (None if (request.form['parent_id'] == '') else (request.form['parent_id']))
    return File.upload(file = request.files['file-0'], parent_id = parent_id)

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
#         file_db.md_tm = time.ctime(os.path.getmtime(root+'/'+filename# ))
#         file_db.ac_tm = time.ctime(os.path.getctime(root+'/'+filename# ))
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
#     db_session.add(file_d# b)
#     tr# y:
#         db_session.commit# ()
#     except PermissionErro# r:
#         result = {"result":#  {
#                 "success": Fals# e,
#                 "error": "Access denied to remove file# "}
#            #  }
#         db_session.rollback#(# )
#
#     return result
