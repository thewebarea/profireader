from flask import render_template, request, g
from .blueprints_declaration import general_bp
from flask.ext.login import current_user


@general_bp.route('')
def index():
    if current_user.is_authenticated():
        portal_base_profireader = 'partials/portal_base_Profireader_auth_user.html'
        profireader_content = 'partials/reader/reader_content.html'
        # portal_id = request.args.get('subscribe', None)
        # print(portal_id)
    else:
        portal_base_profireader = 'partials/portal_base_Profireader.html'
        profireader_content = 'partials/Profireader_content.html'
        # portal_id = None

    return render_template('general/index.html',
                           portal_base_profireader=portal_base_profireader,
                           profireader_content=profireader_content
                           # portal_id=portal_id
                           )
