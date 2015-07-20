#from .db import db
from flask import Flask
from profapp.controllers.views import index
from profapp.controllers.blueprints import user_bp, article_bp, filemanager_bp

def create_app(config='config.ProductionDevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config)
    #db.init_app(app)

    app.add_url_rule('/', 'index', index)

    app.register_blueprint(article_bp, url_prefix='/articles')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(filemanager_bp, url_prefix='/filemanager')

    return app
