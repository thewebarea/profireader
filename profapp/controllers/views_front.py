from .blueprints import front_bp
from flask import render_template, request, url_for, redirect, g
from ..models.articles import Article, ArticlePortal
from ..models.portal import CompanyPortal, PortalDivision
from config import Config



@front_bp.route('/', methods=['GET'])
def index():
    division = g.db().query(PortalDivision).order_by('id').first()
    articles = Article.get_articles_for_portal(
         user_id=g.user_dict['id'], portal_division_id=division.id)
    portal = division.portal.get_client_side_dict()
    return render_template('front/%sindex.html' % (
         portal['layout']['path'],),
         articles={a.id: a.get_client_side_dict() for
                   a in articles},
         division=division.get_client_side_dict(),
         portal=portal)


@front_bp.route('<string:division_name>/<int:page>/'
                '<string:search_text>', methods=['GET'])
def division(division_name, page, search_text):

    search_text = search_text if not request.args.get(
        'search_text') else request.args.get('search_text')
    division = g.db().query(PortalDivision).filter_by(
        name=division_name).one()
    pages = Article.get_pages_count(division.id,
                                    search_text=search_text)
    articles = Article.get_articles_for_portal(
        page_size=Config.ITEMS_PER_PAGE,
        user_id=g.user_dict['id'],
        portal_division_id=division.id, page=page, pages=pages,
        search_text=search_text)
    portal = division.portal.get_client_side_dict()
    return render_template('front/bird/index.html',
                           articles={a.id: a.get_client_side_dict() for
                                     a in articles},
                           division=division.get_client_side_dict(),
                           portal=portal,
                           pages=pages,
                           current_page=page,
                           page_buttons=Config.PAGINATION_BUTTONS,
                           search_text=search_text)

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
