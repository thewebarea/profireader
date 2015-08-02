from flask import render_template, g
from .blueprints import general_bp
from ..constants.USER_REGISTERED import REGISTERED_WITH
#import json

#@general_bp.route('/')
#def hello_world():
#    return render_template('index.html',
#                           id='445548158',
#                           nickname='godsdog',
#                           name='Andriy')


@general_bp.route('')
def index():
    uid = '0'
    name = None
    user = g.user
    if user:
        uid = str(user.id)
        via = user.logged_in_via()
        name = getattr(user, REGISTERED_WITH[via] + '_name')
        #user_params = json.dumps({'id': uid, 'name': name})
    return render_template('index.html',
                           id=uid,
                           name=name)
