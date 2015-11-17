from .blueprints_declaration import reader_bp
from flask import render_template


@reader_bp.route('/', methods=['GET'])
def reader_page():
    return render_template(
        'reader/list.html',
        angular_ui_bootstrap_version='//angular-ui.github.io/bootstrap/ui-bootstrap-tpls-0.14.2.js')
