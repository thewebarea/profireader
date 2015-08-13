from flask import render_template
from flask_wtf.csrf import CsrfProtect

csrf = CsrfProtect()

class Error(Exception):
    pass

class BadCoordinates(Error):
    pass

class BadFormatFile(Error):
    pass

class EmptyFieldName(Error):
    pass

class UserNotFoundError(Error):
    pass

class BadDataProvided(Error):
    pass

@csrf.error_handler
def csrf_error(reason):
    return render_template('errors.html', reason=reason), 400
