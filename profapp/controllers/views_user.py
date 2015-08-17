from .blueprints import user_bp
from flask import url_for, render_template, abort, redirect
from db_init import db_session
from ..models.users import User
from flask.ext.login import current_user, login_required
from ..forms.user import EditProfileForm


#@user_bp.route('/profile/<user_id>', methods=['GET', 'POST'])
#def profile_old(user_id):
#    user_subject = db_session.query(User).filter(User.id == user_id).first()
#    name = user_subject.user_name()
#    user = {'id': user_id, 'name': name}
#    return render_template(url_for('general.index', user=user))


@user_bp.route('/profile/<user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    if current_user != user:
        abort(403)

    form = EditProfileForm()
    if form.validate_on_submit():
        pass
    pass
    return render_template('user_profile.html', form=form, user=g.user_dict)

# @user_bp.route('/delete/<int:x>', methods=['GET', 'POST'])
# def delete(x):
#     return render_template('profile.html', x=x)
