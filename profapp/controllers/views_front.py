from .blueprints import front_bp
from flask import render_template, request, url_for, redirect, g
from ..models.articles import Article
from ..models.portal import CompanyPortal, PortalDivision, PortalDivisionType, Portal



@front_bp.route('/', methods=['GET'])
def index():
    pid = '55e320ea-2389-4001-b176-d068d82e5042'
    division = PortalDivision.get(pid)
    portal = Portal.get(division.portal_id)
    articles = Article.get_articles_for_portal(user_id = g.user_dict['id'], portal_division_id = pid)
    return render_template('front/index.html',
                           articles = {a.id:a.get_client_side_dict() for a in articles},
                           division = division.get_client_side_dict(),
                           portal = portal.get_client_side_dict())
