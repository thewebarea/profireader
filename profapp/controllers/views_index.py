from flask import render_template, g
from .blueprints_declaration import general_bp


@general_bp.route('')
def index():
    return render_template('index.html')
