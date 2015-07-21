from flask import render_template,request, Blueprint

filemanager_bp = Blueprint('filemanager', __name__)

@filemanager_bp.route('/',methods='POST')
@filemanager_bp.route('/',methods='GET')
def filemanager():
    print(request.method)
    #return filemanager_bp.send_static_file('index.html')
    return render_template('filemanager.html')