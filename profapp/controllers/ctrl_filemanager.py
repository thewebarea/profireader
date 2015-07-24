import os
import time
from time import gmtime, strftime
from stat import ST_SIZE
from flask import jsonify, request, Blueprint
from db_connect import sql_session
from profapp.models.files import Files
static_bp = Blueprint('static', __name__, static_url_path='')
root = os.getcwd()+'/profapp/static/filemanager/tmp'
json_result = {"result": {"success": True, "error": None}}

@static_bp.route('/filemanager', methods=['GET', 'POST'])
def ctrl_filemanager():

        try:
            if request.method != 'GET':
                for params in request.json.values():
                    if params['mode'] == 'list':
                        return jsonify(listing(params['path']))
        except AttributeError:
            return jsonify(upload(json_result))

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

def upload(result):

    file = request.files['file-1']
    filename = file.filename
    file_db = Files()
    file.save(os.path.join(root, filename))
    for tmp_file in os.listdir(root):
        st = os.stat(root+'/'+filename)
        file_db.name = filename
        file_db.md_tm = time.ctime(os.path.getmtime(root+'/'+filename))
        file_db.ac_tm = time.ctime(os.path.getctime(root+'/'+filename))
        file_db.cr_tm = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        file_db.size = st[ST_SIZE]
        if os.path.isfile(root+'/'+tmp_file):
            file_db.mime = 'file'
        else:
            file_db.mime = 'dir'
    binary_out = open(root+'/'+filename, 'rb')
    file_db.content = binary_out.read()
    binary_out.close()
    if os.path.isfile(root+'/'+filename):
        os.remove(root+'/'+filename)
    else:
        os.removedirs(root+'/'+filename)
    sql_session.add(file_db)
    try:
        sql_session.commit()
    except PermissionError:
        result = {"result": {
                "success": False,
                "error": "Access denied to remove file"}
            }
        sql_session.rollback()

    return result
