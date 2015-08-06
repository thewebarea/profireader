from flask import render_template, g
from . import blueprints

@blueprints.general_bp.route('')
def index():
    uid = '0'
    name = None
    g_user = g.user
    if g_user:
        uid = g_user.id
        name = g_user.user_name()
    user = {'id': uid, 'name': name}
    return render_template('index.html', user=user)
