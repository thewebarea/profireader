from flask import g, request, url_for, redirect, flash
from werkzeug.exceptions import Unauthorized
from functools import wraps


def admin_required(fn):
    # @wraps(fn)  # do we need it???
    def decorated(*args, **kw):
        if not g.user or not g.user.is_superuser:
            raise Unauthorized('Admin permissions required')
        return fn(*args, **kw)

    return decorated


def login_required(fn):
    @wraps(fn)
    def decorated(*args, **kw):
        if g.user:
            return fn(*args, **kw)
        else:
            flash('Please log in first...', 'error')
            next_url = request.url
            login_url = '%s?next=%s' % (url_for('user.login'), next_url)
            return redirect(login_url)
            #raise Unauthorized('You must be logged in first')
    return decorated
