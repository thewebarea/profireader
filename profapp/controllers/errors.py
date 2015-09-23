from flask import render_template, flash
from flask_wtf.csrf import CsrfProtect
from .blueprints import exception_bp

csrf = CsrfProtect()


class Error(Exception):
    pass


class RightsDefUndefInconsistencyError(Error):
    pass


class ImproperRightsDecoratorUse(Error):
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


class DublicateName(Error):
    pass


class StatusNonActivate(Error):
    pass


class SubscribeToOwn(Error):
    pass

class PortalAlreadyExist(Error):

            # except errors.PortalAlreadyExist as e:
            #     details = e.args[0]
            #     print(details['message'])
    pass


class AlreadyJoined(Error):
    pass


@csrf.error_handler
def csrf_error(reason):
    return render_template('errors/404.html', reason=reason), 400


@exception_bp.errorhandler(404)
def page_not_found(reason):
    return render_template('errors/404.html', reason=reason), 404
