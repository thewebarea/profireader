#from .db import db
from flask import Flask, render_template
from profapp.controllers.views import article_bp, index, filemanager_bp
from profapp.controllers.users_blueprint import users_bp
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def create_app(config='config.ProductionDevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config)
    #db.init_app(app)

    app.add_url_rule('/', 'index', index)

    app.register_blueprint(article_bp, url_prefix='/articles')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(filemanager_bp, url_prefix='/filemanager')\

    return app


#from flask import Flask
#from profapp import views
#app = Flask(__name__)
#app.config.from_object('config')
#
#from profapp import views