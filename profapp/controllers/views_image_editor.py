from .blueprints import image_editor_bp
from flask import render_template

@image_editor_bp.route('/')
def filemanager():
    return render_template('image_editor.html')