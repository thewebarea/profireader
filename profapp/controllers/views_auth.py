from .blueprints import user_bp
from flask import jsonify

@user_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    return jsonify({'a': 'b'})

@user_bp.route('/login/', methods=['GET', 'POST'])
def login():
    return jsonify({'c': 'd'})

@user_bp.route('/login/fb', methods=['GET', 'POST'])
def login_fb():
    return jsonify({'c': 'd'})


#def _session_saver():
#    session.modified = True
#
#
#@user_bp.route('/login/fb/', methods=['GET', 'POST'])
#def login():
#    response = make_response()
#    result = g.authomatic.login(WerkzeugAdapter(request, response), 'fb',
#                                session=session,
#                                session_saver=_session_saver)
#    if result:
#        if result.user:
#            result.user.update()
#            user = User.query.filter_by(fb_id=result.user.id).first()
#            if not user:
#                user = User(result.user.first_name,
#                            result.user.last_name,
#                            result.user.id,
#                            result.user.email)
#                db.session.add(user)
#                db.session.commit()
#            session['user_id'] = user.id
#            return redirect('/')
#
#        elif result.error:
#            redirect_path = '#/?msg={}'.format(quote('Facebook login failed.'))
#            return redirect(redirect_path)
#    return response
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