from flask import render_template, redirect, url_for, request
from profapp import app
from .forms import ArticleForm
from .models.articles import Article, ArticleHistory
from .models.users import User
from profapp.models.company import Company
from db_connect import sql_session
from config import POSTS_PER_PAGE


@app.route('/article/',methods=['GET','POST'])
@app.route('/article/<int:page>',methods=['GET', 'POST'])
def article(page=1):

    form=ArticleForm()
    posts=ArticleHistory.query.filter(ArticleHistory.id==page)

    if form.validate_on_submit():
        article_history=ArticleHistory(form.name.data,form.article.data,0,User.query.first().id)
        sql_session.add(article_history)
        sql_session.commit()

        if len(list(ArticleHistory.query.filter(article_history.name==ArticleHistory.name)))<=1:
            article=Article(User.query.first().id,Company.query.first().id,article_history.id)
            sql_session.add(article)
            sql_session.commit()
        return redirect(url_for('article',page=article_history.id))
    elif request.method!='POST':

        for post in posts:
            form.name.data=post.name
            form.article.data=post.article_text

    return render_template('article.html',
                    form=form,
                    posts=posts
                    )


@app.route('/')
def index():
    return render_template('index.html')
