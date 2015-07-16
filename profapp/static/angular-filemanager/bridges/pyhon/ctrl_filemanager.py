from profapp.controllers.views import filemanager_bp
@filemanager_bp.route('/',methods=['GET','POST'])
def filemanager():
    return filemanager_bp.send_static_file('index.html')