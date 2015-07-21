import os
from time import gmtime, strftime
from stat import *
from flask import jsonify, request, Blueprint

files = os.listdir('/home/viktor/Downloads')
static_bp = Blueprint('static', __name__)

@static_bp.route('/filemanager/bridges/python/ctrl_filemanager.py', methods=['GET', 'POST'])
def ctrl_filemanager():
    for params in request.json.values():
        if params['mode'] == 'list':
            print(listing())
            return jsonify(listing())



def listing():

    info = []
    for file in files:
        st = os.stat('/home/viktor/Downloads/'+file)
        params = dict()
        params['size'] = st[ST_SIZE]
        params['date'] = strftime("%Y-%d-%m %X", gmtime(st[ST_MTIME]))
        params['name'] = os.path.basename(file)
        params['rights'] = 'drwxr-xr-x'
        if os.path.isfile('/home/viktor/Downloads/'+file):
            params['type'] = 'file'
        else :
            params['type'] = 'dir'
        info.append(params)
    file_list = {"result": info}
    return file_list


