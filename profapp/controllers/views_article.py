from flask import render_template, redirect, url_for, request, g
from profapp.forms.article import ArticleForm
from profapp.models.articles import Article, ArticleCompany
from profapp.models.users import User
# from profapp.models.company import Company
# from db_init import db_session
from .blueprints import article_bp
from .request_wrapers import ok, object_to_dict
# import os


def _A():
    return g.db.query(Article)


def _C():
    return g.db.query(ArticleCompany)


@article_bp.route('/list/', methods=['GET'])
def show_mine():
    return render_template('article/list.html')


@article_bp.route('/list/', methods=['POST'])
@ok
def load_mine(json):
    return {'articles': [a.get_client_side_dict() for a in Article.get_articles_for_user(g.user.id)]}


@article_bp.route('/create/', methods=['GET'])
def show_form_create():
    return render_template('article/create.html')


@article_bp.route('/create/', methods=['POST'])
@ok
def load_form_create(json):
    return {'id': '', 'title': '', 'short': '', 'long': ''}


@article_bp.route('/confirm_create/', methods=['POST'])
@ok
def confirm_create(json):
    return Article.save_new_article(g.user_dict['id'], **json). \
        get_client_side_dict()


@article_bp.route('/update/<string:article_company_id>/',
                  methods=['GET'])
def show_form_update(article_company_id):
    return render_template('article/update.html',
                           article_company_id=article_company_id)


@article_bp.route('/update/<string:article_company_id>/',
                  methods=['POST'])
@ok
def load_form_update(json, article_company_id):
    return ArticleCompany.get(article_company_id).get_client_side_dict()


@article_bp.route('/save/<string:article_company_id>/',
                  methods=['POST'])
@ok
def save(json, article_company_id):
    return Article.save_edited_version(g.user.id, article_company_id,
                                       **json).get_client_side_dict()


@article_bp.route('/details/<string:article_id>/', methods=['GET'])
def details(article_id):
    return render_template('article/details.html',
                           article_id=article_id)


@article_bp.route('/details/<string:article_id>/', methods=['POST'])
@ok
def details_load(json, article_id):
    return Article.get(article_id).get_client_side_dict()


@article_bp.route('/search_for_company_to_submit/', methods=['POST'])
@ok
def search_for_company_to_submit(json):
    companies = Article().search_for_company_to_submit(
        g.user_dict['id'], json['article_id'], json['search'])
    return companies


@article_bp.route('/submit_to_company/<string:article_id>/',
                  methods=['POST'])
@ok
def submit_to_company(json, article_id):
    a = Article.get(article_id)
    a.mine.clone_for_company(json['company_id'])
    return {'article': a.get(article_id).get_client_side_dict(),
            'company_id': json['company_id']}
