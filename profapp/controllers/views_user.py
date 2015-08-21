from .blueprints import user_bp
from flask import url_for, render_template, abort, redirect
from db_init import db_session
from ..models.users import User
from flask.ext.login import current_user, login_required
from ..forms.user import EditProfileForm
from flask import g


#@user_bp.route('/profile/<user_id>', methods=['GET', 'POST'])
#def profile_old(user_id):
#    user_subject = db_session.query(User).filter(User.id == user_id).first()
#    name = user_subject.user_name()
#    user = {'id': user_id, 'name': name}
#    return render_template(url_for('general.index', user=user))


@user_bp.route('/profile/<user_email>')
@login_required
def profile(user_email):
    user = db_session.query(User).\
        filter(User.profireader_email == user_email).first()
    if not user:
        abort(404)
    if current_user != user:
        abort(403)
    form = EditProfileForm()
    if form.validate_on_submit():
        pass
    pass
    return render_template('user_profile.html', form=form)


@user_bp.route('/edit-profile/<user_email>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_email):
    user = db_session.query(User).\
        filter(User.profireader_email == user_email).first()
    if not user:
        abort(404)
    if current_user != user:
        abort(403)
    return render_template('user_edit_profile.html')
