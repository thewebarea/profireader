from flask import render_template
from .blueprints import filemanager_bp

@filemanager_bp.route('/filemanager')
def filemanager():
    return render_template('filemanager.html')
