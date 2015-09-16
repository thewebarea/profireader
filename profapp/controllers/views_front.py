from .blueprints import front_bp
from flask import render_template, request, url_for, redirect, g, current_app
from ..models.articles import Article, ArticlePortal
from ..models.portal import CompanyPortal, PortalDivision, Portal
from config import Config
# from profapp import

@front_bp.route('/', methods=['GET'])
def index():

    page = 1
    search_text = ''
    app = current_app._get_current_object()
    portal = g.db().query(Portal).filter_by(host=app.config['SERVER_NAME']).one()
    # pages = Article.get_pages_count(division.id,
    #                                 search_text=search_text)
    articles = Article.get_articles_for_portal(
        page_size=Config.ITEMS_PER_PAGE,
        user_id=g.user_dict['id'],
        page=page, pages=[],
        portal_id = portal.id,
        search_text=search_text)

    return render_template('front/bird/index.html',
                           articles={a.id: a.get_client_side_dict() for
                                     a in articles},
                           division=None,
                           portal=portal,
                           page=1,
                           pages=1,
                           current_page=page,
                           page_buttons=Config.PAGINATION_BUTTONS,
                           search_text=search_text)


@front_bp.route('<string:division_name>/<int:page>/'
                '<string:search_text>', methods=['GET'])
def division(division_name, page, search_text):

    app = current_app._get_current_object()
    portal = g.db().query(Portal).filter_by(host=app.config['SERVER_NAME']).one()
    search_text = search_text if not request.args.get(
        'search_text') else request.args.get('search_text')
    division = g.db().query(PortalDivision).filter_by(
        portal_id=portal.id, name=division_name).one()
    pages = Article.get_pages_count(division.id,
                                    search_text=search_text)
    articles = Article.get_articles_for_portal(
        page_size=Config.ITEMS_PER_PAGE,
        user_id=g.user_dict['id'],
        portal_division_id=division.id, page=page, pages=pages,
        search_text=search_text)

    return render_template('front/bird/division.html',
                           articles={a.id: a.get_client_side_dict() for
                                     a in articles},
                           division=division.get_client_side_dict(),
                           portal=portal,
                           pages=pages,
                           current_page=page,
                           page_buttons=Config.PAGINATION_BUTTONS,
                           search_text=search_text)

# TODO OZ by OZ: portal filter, move portal filtering to decorator

@front_bp.route('details/<string:article_portal_id>')
def details(article_portal_id):
    article = ArticlePortal.get(article_portal_id).\
        to_dict('id, title,short, cr_tm, md_tm, '
                'publishing_tm, status, long,'
                'division.name, division.portal.id,'
                'company.name')
    return render_template('front/bird/article_details.html',
                           article=article,
                           portal=article['division']['portal']
                           )
