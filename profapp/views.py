from flask import render_template
from profireader import app
from .forms import ArticleForm
from .models.articles import Article, ArticleHistory
from .models.users import User
from db_connect import sql_session

@app.route('/article',methods=['GET', 'POST'])
def article():
    form=ArticleForm()
    if form.validate_on_submit():
        article=Article(sql_session.query(User).first())
        article_history=ArticleHistory(form.article.data,0,article.author_user_id)
        sql_session.add_all([article,article_history])
        sql_session.commit()

    return render_template('article.html',
                    form=form
                    )