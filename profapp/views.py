from flask import render_template
from profapp import app
from .forms import ArticleForm
from profapp.models.articles import Article, ArticleHistory
from profapp.models.users import User
from profapp.models.company import Company
from db_connect import sql_session


@app.route('/article', methods=['GET', 'POST'])
def article_getpost():
    form = ArticleForm()
    if form.validate_on_submit():
        article = Article(author_user_id=User.query.first().id,
                          company_id=Company.query.first().id)
        article_history = ArticleHistory(form.article.data, 0,
                                         User.query.first().id)
        sql_session.add_all([article, article_history])
        sql_session.commit()

    return render_template('article.html', form=form)


@app.route('/')
def index():
    return render_template('index.html')
