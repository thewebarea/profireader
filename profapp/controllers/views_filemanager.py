import os
import time
from time import gmtime, strftime
from stat import ST_SIZE
from flask import jsonify, request, render_template
from db_init import db_session
from profapp.models.files import File
from .blueprints import filemanager_bp, static_bp

root = os.getcwd()+'/profapp/static/filemanager/tmp'
json_result = {"result": {"success": True, "error": None}}

@filemanager_bp.route('/')
def filemanager():
    return render_template('filemanager.html')

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
    for file in db_session.query(File).filter():
        date = str(file.md_tm)
        date = date.split('.')
        params = dict()
        params['size'] = file.size
        params['date'] = date[0]
        params['name'] = file.name
        params['rights'] = 'drwxr-xr-x'
        params['id'] = file.id
        if file.mime == 'dir':
            params['type'] = 'dir'
        else:
            params['type'] = 'file'
        info.append(params)
    result = {"result": info}
    return result

def upload(result):

    for l in range(len(request.files)):
        file = request.files['file-%s' % (l+1)]
        filename = file.filename
        file_db = File()
        file.save(os.path.join(root, filename))
        for tmp_file in os.listdir(root):
            st = os.stat(root+'/'+filename)
            file_db.name = filename
            file_db.md_tm = time.ctime(os.path.getmtime(root+'/'+filename))
            file_db.ac_tm = time.ctime(os.path.getctime(root+'/'+filename))
            file_db.cr_tm = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            file_db.size = st[ST_SIZE]
            if os.path.isdir(root+'/'+tmp_file):
                file_db.mime = 'dir'
            else:
                file_db.mime = file.mimetype
        with open(root+'/'+filename, 'rb') as f:
            file_db.content = bytearray(f.read())
        if os.path.isfile(root+'/'+filename):
            os.remove(root+'/'+filename)
        else:
            os.removedirs(root+'/'+filename)
        db_session.add(file_db)
    try:
        db_session.commit()
    except PermissionError:
        result = {"result": {
                "success": False,
                "error": "Access denied to upload file"}
            }
        db_session.rollback()

    return result
