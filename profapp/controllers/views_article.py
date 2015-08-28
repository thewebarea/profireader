from flask import render_template, redirect, url_for, request, g
from profapp.forms.article import ArticleForm
from profapp.models.articles import Article, ArticleCompany
from profapp.models.users import User
from profapp.models.company import Company
from db_init import db_session
from .blueprints import article_bp
from .request_wrapers import json, object_to_dict
#import os


def _A():
    return db_session.query(Article)


def _C():
    return db_session.query(ArticleCompany)

@article_bp.route('/list/', methods=['GET'])
def show_mine():
    return render_template('article/list.html', articles = _A().filter_by(author_user_id=g.user_dict['id']).all())

@article_bp.route('/create/', methods=['GET'])
def show_form_create():
    return render_template('article/create.html', edit_version = {'title': '', 'short':  '', 'long': ''})

@article_bp.route('/create/', methods=['POST'])
def create():
    return redirect(url_for('article.details',
                            article_id=Article.save_new_article(g.user.id, **request.form.to_dict(True)).id))

@article_bp.route('/update/<string:article_company_id>/', methods=['GET'])
def show_form_update(article_company_id):
    article_for_company = ArticleCompany.get(article_company_id)
    company = article_for_company.company.__dict__ if article_for_company.company else {}
    return render_template('article/update.html', edit_version = article_for_company.__dict__, company = company)

@article_bp.route('/update/<string:article_company_id>/', methods=['POST'])
def update(article_company_id):
    return redirect(url_for('article.details',
                            article_id = Article.save_edited_version(g.user.id, article_company_id, **request.form.to_dict(True)).article_id))

@article_bp.route('/details/<string:article_id>/', methods=['GET'])
def details(article_id):
    article = Article.get(article_id)
    d = object_to_dict(article, 'id', 'mine.id', 'submitted.id', 'submitted.cr_tm', 'submitted.editor', '*')
    return render_template('article/details.html', article = object_to_dict(article, 'id', 'mine.id', 'submitted.id', 'submitted.cr_tm', 'submitted.editor', '*'))


@article_bp.route('/search_for_company_to_submit/', methods=['POST'])
@json
def search_for_company_to_submit(json):
    companies = Company().search_for_company(g.user_dict['id'], json['search'])
    return companies

@article_bp.route('/submit_to_company/<string:article_id>/', methods=['POST'])
@json
def submit_to_company(json, article_id):
    a = Article.get(article_id)
    a.mine.clone_for_company(json['company_id'])
    return [s.dict() for s in Article.get(article_id).submitted]
