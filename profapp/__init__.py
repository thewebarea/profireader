#from .db import db
from flask import Flask, render_template
from profapp.controllers.views import article_bp, index
#from profapp import views

def create_app(config='config.ProductionDevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config)
    #db.init_app(app)

    app.add_url_rule('/', 'index', index)

    app.register_blueprint(article_bp, url_prefix='/articles')
    return app


#from flask import Flask
#from profapp import views
#app = Flask(__name__)
#app.config.from_object('config')
#
#from profapp import views