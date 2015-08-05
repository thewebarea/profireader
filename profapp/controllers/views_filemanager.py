import os
import time
from time import gmtime, strftime
from stat import ST_SIZE
from flask import jsonify, request, render_template, make_response, send_file
from db_init import db_session, engine
from profapp.models.files import File, FileContent
from .blueprints import filemanager_bp, static_bp
from io import BytesIO
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
        file_content = FileContent()
        file_db = File()
        file = request.files['file-%s' % (l+1)]
        filename = file.filename
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
            file_content.content = bytearray(f.read())
        if os.path.isfile(root+'/'+filename):
            os.remove(root+'/'+filename)
        else:
            os.removedirs(root+'/'+filename)
        db_session.add(file_db)
        if True:
            db_session.commit()
            file_content.file_id = file_db.id
            db_session.add(file_content)
            db_session.commit()
        else:
            db_session.rollback()
            raise PermissionError

    return result

@filemanager_bp.route('/get/<string:id>')
def get(id):
    image_query = file_query(id, File)
    image_query_content = db_session.query(FileContent).filter_by(file_id=id).first()
    response = make_response()
    response.headers['Content-Type'] = image_query.mime
    response.headers['Content-Disposition'] = 'filename=%s' % image_query.name
    return send_file(BytesIO(image_query_content.content), mimetype=image_query.mime, as_attachment=False)

def file_query(id, table):
    if db_session.query(table).filter_by(id=id).first():
        query = db_session.query(table).filter_by(id=id).first()

        return query
    else:
        return "404 error", 404
