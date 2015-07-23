import os
from time import gmtime, strftime
from flask import jsonify, request, Blueprint
from db_connect import sql_session
from profapp.models.files import Files
static_bp = Blueprint('static', __name__, static_url_path='')
root = os.getcwd()+'/profapp/static/filemanager/files'
json_result = {"result": {"success": True, "error": None}}

@static_bp.route('/filemanager', methods=['GET', 'POST'])
def ctrl_filemanager():

    if request.method != 'GET':

        for params in request.json.values():
            if params['mode'] == 'list':
                return jsonify(listing(params['path']))


def listing(folder_path):

    info = []
    for file in sql_session.query(Files).filter():
        date = str(file.md_tm)
        date = date.split('.')
        params = dict()
        params['size'] = file.size
        params['date'] = date[0]
        params['name'] = file.name
        params['rights'] = 'drwxr-xr-x'
        params['id'] = file.id
        if file.mime == 'directory':
            params['type'] = 'dir'
        else:
            params['type'] = 'file'
        info.append(params)
    result = {"result": info}
    return result

