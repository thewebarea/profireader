from flask import Flask, session, g
from authomatic.providers import oauth2
from authomatic import Authomatic
from profapp.models.users import User
from profapp.controllers.blueprints import register as register_blueprints
from flask import url_for


def setup_authomatic(app):
    authomatic = Authomatic(app.config['OAUTH_CONFIG'],
                            app.config['SECRET_KEY'],
                            report_errors=True)

    def func():
        g.authomatic = authomatic
    return func


def load_user():
    g.user = None
    if 'user_id' in session.keys():
        g.user = User.query.filter_by(id=session['user_id']).first()


def flask_endpoint_to_angular(endpoint, **kwargs):
    options = {}
    for kw in kwargs:
        options[kw] = "{{" + "{0}".format(kwargs[kw]) + "}}"
    url = url_for(endpoint, **options)
    import urllib.parse
    url = urllib.parse.unquote(url)
    url = url.replace('{{', '{{ ').replace('}}', ' }}')
    return url


def create_app(config='config.ProductionDevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config)

    app.before_request(setup_authomatic(app))
    app.before_request(load_user)
    register_blueprints(app)

    # read this: http://stackoverflow.com/questions/6036082/call-a-python-function-from-jinja2
    app.jinja_env.globals.update(flask_endpoint_to_angular=flask_endpoint_to_angular)

    # see: http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/
    # Flask will automatically remove database sessions at the end of the
    # request or when the application shuts down:
    from db_init import db_session

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
