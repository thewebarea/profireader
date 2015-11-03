import os
from flask import render_template, g, make_response
from flask.ext.login import current_user
from profapp.models.files import File
from .blueprints import filemanager_bp
from .request_wrapers import ok
from functools import wraps
from time import sleep
from flask import jsonify
import json as jsonmodule
from ..models.google import YoutubeApi
from flask import session, redirect, request, url_for
from ..models.google import GoogleAuthorize, GoogleToken
from utils.db_utils import db
from ..models.company import Company

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


@filemanager_bp.route('/uploader/', methods=['GET', 'POST'])
@filemanager_bp.route('/uploader/<string:company_id>', methods=['GET', 'POST'])
def uploader(company_id=None):

    token_db_class = GoogleToken()
    credentials_exist = token_db_class.check_credentials_exist()
    google = GoogleAuthorize()
    if not credentials_exist and google.check_admins():
        if 'code' in request.args:
            session['auth_code'] = request.args['code']
            token_db_class.save_credentials()
        return redirect(url_for('company.show')) if 'code' in request.args \
            else redirect(google.get_auth_code())
    return render_template('file_uploader.html', company_id=company_id)


@filemanager_bp.route('/send/<string:company_id>/', methods=['POST'])
def send(company_id):
    """ YOU SHOULD SEND PROPERTY NAME, DESCRIPTION, ROOT_FOLDER AND FOLDER.
    NOW THIS VALUES GET FROM DB. HARDCODE!!! """
    company = db(Company, id=company_id).one() ## HARD CODE
    file = request.files['file']
    data = request.form
    body = {'title': file.filename,
            'description': 'TESTING', ## HARD CODE
            'status': 'public'}

    youtube = YoutubeApi(body_dict=body,
                         video_file=file.stream.read(-1),
                         chunk_info=dict(chunk_size=int(data.get('chunkSize')),
                                         chunk_number=int(data.get('chunkNumber')),
                                         total_size=int(data.get('totalSize'))),
                         company_id=company_id,
                         root_folder_id=company.journalist_folder_file_id, ## HARD CODE
                         parent_folder_id=company.journalist_folder_file_id) ## HARD CODE
    youtube.upload()
    return jsonify({'result': {'size': 0}})


@filemanager_bp.route('/resumeopload/', methods=['GET'])
def resumeopload():

    return jsonify({'size': 0})
