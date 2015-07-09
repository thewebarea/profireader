from flask.ext.wtf import Form
from wtforms import TextAreaField
from wtforms.validators import DataRequired

class ArticleForm(Form):
    article=TextAreaField('article',validators=[DataRequired()])