from .blueprints_declaration import auth_bp
from flask import g, request, url_for, render_template, flash, current_app, session
#from db_init import db_session
from ..constants.SOCIAL_NETWORKS import DB_FIELDS, SOC_NET_FIELDS, \
    SOC_NET_FIELDS_SHORT
from flask.ext.login import logout_user, current_user, login_required
from urllib.parse import quote
from ..models.users import User
from ..forms.auth import LoginForm, RegistrationForm, ChangePasswordForm, \
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from .errors import BadDataProvided
from ..utils.email import send_email

import re
from authomatic.adapters import WerkzeugAdapter

from flask import redirect, make_response
from flask.ext.login import login_user
from ..constants.SOCIAL_NETWORKS import SOC_NET_NONE
from ..constants.UNCATEGORIZED import AVATAR_SIZE, AVATAR_SMALL_SIZE

# def _session_saver():
#    session.modified = True

EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')


def login_signup_general(*soc_network_names):
    if g.user_init and g.user_init.is_authenticated():
        raise BadDataProvided

    response = make_response()
    try:
        result = g.authomatic.login(WerkzeugAdapter(request, response),
                                    soc_network_names[-1])
        if result:
            if result.user:
                result.user.update()
                result_user = result.user
                if result_user.email is None:
                    flash("you haven't confirm email bound to your "
                          "soc-network account yet. "
                          "Please confirm email first or choose "
                          "another way of authentication.")
                    redirect(url_for('auth.login'))

                db_fields = DB_FIELDS[soc_network_names[-1]]
                #user = g.db.query(User).\
                #    filter(getattr(User, db_fields['id']) == result_user.id)\
                #    .first()
                user = g.db.query(User).\
                    filter(getattr(User, db_fields['email']) == result_user.email)\
                    .first()
                if not user:
                    user = g.db.query(User).\
                        filter(User.profireader_email == result_user.email)\
                        .first()
                    ind = False
                    if not user:
                        ind = True
                        user = User()
                    for elem in SOC_NET_FIELDS:
                        setattr(user, db_fields[elem],
                                getattr(result_user, elem))

                    if ind:  # ToDo (AA): introduce field signup_via instead.
                        # Todo (AA): If signed_up not via profireader then...
                        if soc_network_names[0] == 'profireader':
                            db_fields_profireader = DB_FIELDS['profireader']
                            for elem in SOC_NET_FIELDS_SHORT:
                                setattr(user, db_fields_profireader[elem],
                                        getattr(result_user, elem))
                        user.profireader_avatar_url = \
                            user.avatar(size=AVATAR_SIZE)
                        user.profireader_small_avatar_url = \
                            user.avatar(size=AVATAR_SMALL_SIZE)

                    g.db.add(user)
                    user.confirmed = True
                    g.db.commit()

                if user.is_banned():
                    flash('Sorry, you cannot login into the Profireader. Contact the profireader'
                          'administrator, please: ' +
                          current_app.config['PROFIREADER_MAIL_SENDER'])

                    return redirect(url_for('general.index'))

                login_user(user)
                session['logged_via'] = soc_network_names
                flash('You have successfully logged in.')

                # session['user_id'] = user.id assignment
                # is automatically executed by login_user(user)

                return redirect('/')  # #  http://aprofi.d.ntaxa.com/
            elif result.error:
                redirect_path = '#/?msg={}'.\
                    format(quote(soc_network_names[-1] + ' login failed.'))
                return redirect(redirect_path)
    except:
        import sys
        print(sys.exc_info())
        raise
    return response


@auth_bp.before_app_request
def before_request():
    if current_user.is_authenticated():
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth_bp.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous() or current_user.confirmed:
        return redirect(url_for('general.index'))
    return render_template('auth/unconfirmed.html')


@auth_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    # if g.user_init and g.user_init.is_authenticated():
    if g.user_init.is_authenticated():
        if request.method != 'GET':
            # raise BadDataProvided
            flash('You are already logged in.'
                  'To sign up Profireader with new account you '
                  'should logout first')
            return redirect(url_for('auth.signup'))
        portal_id = request.args.get('subscribe', None)
        if portal_id:
            return redirect(url_for('general.reader_subscription', portal_id=portal_id))

    form = RegistrationForm()
    if form.validate_on_submit():  # # pass1 == pass2
        profireader_all = SOC_NET_NONE['profireader'].copy()
        profireader_all['email'] = form.email.data
        profireader_all['name'] = form.displayname.data
        user = User(
            PROFIREADER_ALL=profireader_all,
            password=form.password.data  # # pass is automatically hashed
        )
        user.profireader_avatar_url = \
            user.avatar(size=AVATAR_SIZE)
        user.profireader_small_avatar_url = \
            user.avatar(size=AVATAR_SMALL_SIZE)
        # # user.password = form.password.data  # pass is automatically hashed

        g.db.add(user)
        g.db.commit()
        token = user.generate_confirmation_token()
        send_email(user.profireader_email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)


@auth_bp.route('/login/<soc_network_name>', methods=['GET', 'POST'])
def login_soc_network(soc_network_name):
    #return login_signup_general(soc_network_name)
    return login_signup_general('profireader', soc_network_name)


@auth_bp.route('/signup/<soc_network_name>', methods=['GET', 'POST'])
def signup_soc_network(soc_network_name):
    return redirect(url_for('auth.login_soc_network',
                     soc_network_name=soc_network_name))
    #return login_signup_general('profireader', soc_network_name)


# read: flask.ext.login
# On a production server, the login route must be made available over
# secure HTTP so that the form data transmitted to the server is en‐
# crypted. Without secure HTTP, the login credentials can be intercep‐
# ted during transit, defeating any efforts put into securing passwords
# in the server.
#
# read this!: http://flask.pocoo.org/snippets/62/
@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    # if g.user_init and g.user_init.is_authenticated():
    portal_id = request.args.get('subscribe', None)
    if g.user_init.is_authenticated():
        if portal_id:
            return redirect(url_for('general.reader_subscription', portal_id=portal_id))
        flash('You are already logged in. If you want to login with another '
              'account logout first please')
        return redirect(url_for('general.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = g.db.query(User).\
            filter(User.profireader_email == form.email.data).first()

        if user and user.is_banned():
            return redirect(url_for('general.index'))
        if user and user.verify_password(form.password.data):
            login_user(user)
            if portal_id:
                return redirect(url_for('general.reader_subscription', portal_id=portal_id))
            return redirect(request.args.get('next') or url_for('general.index'))
        flash('Invalid username or password.')
        redirect_url = url_for('auth.login')
        redirect_url += '?/' + portal_id if portal_id else ''
        return redirect(redirect_url)
    return render_template('auth/login.html', form=form, portal_id=portal_id)


@auth_bp.route('/logout/', methods=['GET'])
@login_required   # Only logged in user can be logged out
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('general.index'))


@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('general.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('general.index'))


@auth_bp.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.profireader_email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('general.index'))


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            g.db.add(current_user)
            g.db.commit()
            flash('Your password has been updated.')
            return redirect(url_for('general.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


@auth_bp.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous():
        flash('To reset your password logout first please.')
        return redirect(url_for('general.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = g.db.query(User).\
            filter_by(profireader_email=form.email.data).first()
        if user.is_banned():
            return redirect(url_for('general.index'))
        if user:
            token = user.generate_reset_token()
            send_email(user.profireader_email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
            flash('An email with instructions to reset your password has been '
                  'sent to you.')
        else:
            flash('You are not Profireader user yet. Sign up Profireader '
                  'first please.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth_bp.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous():
        return redirect(url_for('general.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = g.db.query(User).\
            filter_by(profireader_email=form.email.data).first()
        if (user is None) or user.is_banned():
            return redirect(url_for('general.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('general.index'))
    return render_template('auth/reset_password_token.html', form=form,
                           token=token)


@auth_bp.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('general.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)


@auth_bp.route('/change-email/<tokren>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.')
        g.db.add(current_user)
        g.db.commit()
    else:
        flash('Invalid request.')
    return redirect(url_for('general.index'))
