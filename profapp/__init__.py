#from .db import db
from flask import Flask
from profapp.controllers.views import article_bp, index, filemanager_bp
from profapp.controllers.ctrl_filemanager import static_bp
#from profapp import views

def create_app(config='config.ProductionDevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config)
    #db.init_app(app)

    app.add_url_rule('/', 'index', index)
    app.register_blueprint(static_bp,url_prefix='/static')
    app.register_blueprint(article_bp, url_prefix='/articles')
    app.register_blueprint(filemanager_bp, url_prefix='/filemanager')
    return app


#from flask import Flask
#from profapp import views
#app = Flask(__name__)
#app.config.from_object('config')
#
#from profapp import views
