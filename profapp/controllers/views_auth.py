from .blueprints import user_bp
from flask import jsonify, make_response, g, session, request, redirect, \
    url_for, render_template
from authomatic.adapters import WerkzeugAdapter
from ..models.users import User
from db_init import db_session
from ..constants.USER_REGISTERED import REGISTERED_WITH_FLIPPED
from ..constants.SOCIAL_NETWORKS import DB_FIELDS, SOC_NET_FIELDS
import sqlalchemy.exc as sqlalchemy_exc

from urllib.parse import quote

#def _session_saver():
#    session.modified = True

import re
from authomatic.adapters import WerkzeugAdapter

from flask import redirect, make_response
from flask.ext.login import login_user


EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')


#provider_name:
# 0) profireader+
# 1) facebook +-
# 2) linkedin +
# 3) google +
# 4) twitter +
# 5) microsoft +
# 6) yahoo +


@user_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    uid = '0'
    name = None
    user = g.user
    if user:
        uid = str(user.id)
        name = user.user_name()
        #user_params = json.dumps({'id': uid, 'name': name})
    return render_template('signup.html',
                           id=uid,
                           name=name)

@user_bp.route('/login/', methods=['GET', 'POST'])
def login():
    uid = '0'
    name = None
    user = g.user
    if user:
        uid = str(user.id)
        name = user.user_name()
        #user_params = json.dumps({'id': uid, 'name': name})
    return render_template('login.html',
                           id=uid,
                           name=name)


# TODO: just complete this
# TODO: if registration was via email
# TODO: we should make validation!

# TODO: consider the situation when
# TODO: we have really profile_completed = True
# TODO: it is only possible when user was registered
# TODO: via email
# email_conf_key=None, email_conf_tm=None, pass_reset_key=None,
# pass_reset_conf_tm=None, registered_via=None, ):
@user_bp.route('/login/profireader', methods=['GET', 'POST'])
def login_profireader():
    #  email = result.user.email
    #  if email and EMAIL_REGEX.match(email):
    #      user = User.query.filter_by(email=email).first()
    #      if user:
    #          login_user(user)
    #          return redirect(url_for('general.index'))
    #      return redirect(url_for('general.index'))  #  delete this redirect
    return render_template('login.html')


# it is valid only if registration was via soc network
@user_bp.route('/login/<provider_name>', methods=['GET', 'POST'])
def login_soc_network(provider_name):
    response = make_response()
    try:
        result = g.authomatic.login(WerkzeugAdapter(request, response),
                                    provider_name)
        if result:
            if result.user:
                result.user.update()
                result_user = result.user
                db_fields = DB_FIELDS[provider_name.upper()]
                user = db_session.query(User).\
                    filter(getattr(User, db_fields['ID']) == result_user.id)\
                    .first()
                if not user:
                    user = User(
                        registered_via=REGISTERED_WITH_FLIPPED[provider_name]
                    )
                    for elem in SOC_NET_FIELDS:
                        setattr(user, db_fields[elem],
                                getattr(result_user, elem.lower()))
                    db_session.add(user)
                    db_session.commit()
                session['user_id'] = user.id

                return redirect('/')  # #  http://aprofi.d.ntaxa.com/
                #return redirect('https://www.yahoo.com', code=302)
            elif result.error:
                redirect_path = '#/?msg={}'.\
                    format(quote(provider_name + ' login failed.'))
                return redirect(redirect_path)

    except:
        import sys
        print(sys.exc_info())
        raise
    return response

#
#
#@user_bp.route('/user-info/', methods=['GET'])  # user profile
#def user_info():
#    res = {}
#    if g.user:
#        res = (
#            {'id': g.user.id, 'first_name': g.user.fb_first_name,
#             'last_name': g.user.fb_last_name,
#             'fb_id': g.user.fb_id,
#             'email': g.user.email})
#    return jsonify(res)
#
#

#@user_bp.route('/logout/', methods=['GET'])
#def logout():
#    session.pop('authomatic:fb:state', None)
#    session.pop('user_id', None)
#    return jsonify({}), 200