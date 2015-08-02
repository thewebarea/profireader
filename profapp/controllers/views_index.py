from flask import render_template, g
from .blueprints import general_bp
import json

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
    #logged_in = 'false'
    if g.user:
        uid = str(g.user.id)
        #name = g.user.name
        #name = u'Андрій Андрусик'
        name = 'Andriy'
        #logged_in = 'true'
        #user_params = json.dumps({'id': uid, 'name': name})
        #print(user_params)
    return render_template('index.html',
                           id=uid,
                           name=name)
