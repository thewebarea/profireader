from flask import Flask
#from profapp import views

app = Flask(__name__)
app.config.from_object('config')

from profapp import views
