from .blueprints import front_bp
from flask import render_template, request, url_for, redirect, g
from ..models.articles import Article
from ..models.portal import CompanyPortal, PortalDivision, \
    PortalDivisionType, Portal
# from db_init import Base
from config import Config



# @front_bp.route('/', methods=['GET'])
# def index():
#     division = g.db().query(PortalDivision).order_by('id').first()
#     articles = Article.get_articles_for_portal(
#         user_id=g.user_dict['id'], portal_division_id=division.id)
#     portal = division.portal.get_client_side_dict()
#     return render_template('front/%sindex.html' % (
#         portal['layout']['path'],),
#         articles={a.id: a.get_client_side_dict() for
#                   a in articles},
#         division=division.get_client_side_dict(),
#         portal=portal)


@front_bp.route('<string:division_name>/<int:page>', methods=['GET'])
def division(division_name, page):
    division = g.db().query(PortalDivision).filter_by(
        name=division_name).one()
    pages = Article.get_pages_count(division.id)
    articles = Article.get_articles_for_portal(
        page_size=Config.ITEMS_PER_PAGE,
        user_id=g.user_dict['id'],
        portal_division_id=division.id, page=page, pages=pages)
    # articles = Article.pagination(obj=articles, page=page,
    #                               items_per_page=Config.ITEMS_PER_PAGE)
    portal = division.portal.get_client_side_dict()
    return render_template('front/bird/index.html',
                           articles={a.id: a.get_client_side_dict() for
                                     a in articles},
                           division=division.get_client_side_dict(),
                           portal=portal,
                           pages=pages,
                           current_page=page,
                           page_buttons=Config.PAGINATION_BUTTONS)
