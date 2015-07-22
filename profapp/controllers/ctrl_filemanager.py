import os
from time import gmtime, strftime
from stat import ST_MTIME, ST_SIZE
from flask import jsonify, request, Blueprint

static_bp = Blueprint('static', __name__)
root = '/home/viktor/Downloads'
json_result = {"result": {"success": True, "error": None}}

@static_bp.route('/filemanager/bridges/python/ctrl_filemanager.py', methods=['GET', 'POST'])
def ctrl_filemanager():

    for params in request.json.values():
        if params['mode'] == 'list':
            return jsonify(listing())
        elif params['mode'] == 'rename':
            return jsonify(rename(params['path'], params['newPath'], json_result))
        elif params['mode'] == 'delete':
            return jsonify(remove(params['path'], json_result))
        elif params['mode'] == 'editfile':
            return jsonify(get_content(params['path']))

def listing():

    info = []
    files = os.listdir(root)
    for file in files:
        st = os.stat(root+'/'+file)
        params = dict()
        params['size'] = st[ST_SIZE]
        params['date'] = strftime("%Y-%d-%m %X", gmtime(st[ST_MTIME]))
        params['name'] = os.path.basename(file)
        params['rights'] = 'drwxr-xr-x'
        if os.path.isfile(root+'/'+file):
            params['type'] = 'file'
        else:
            params['type'] = 'dir'
        info.append(params)
    result = {"result": info}
    return result

def rename(path, new_path, result):

    os.renames(root+path, root+new_path)
    return result

def remove(file, result):

    if os.path.isfile(root+file):
        os.remove(root+file)
    else:
        os.removedirs(root+file)
    return result

def get_content(file):

    opener = open(root+file)
    reader = opener.read()
    result = {"result": reader}
    return result