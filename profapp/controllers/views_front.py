from .blueprints import front_bp
from flask import render_template, request, url_for, redirect, g, current_app
from ..models.articles import Article, ArticlePortal
from ..models.portal import CompanyPortal, PortalDivision, Portal, Company
from config import Config
# from profapp import
from .pagination import pagination

@front_bp.route('/', methods=['GET'])
@front_bp.route('<int:page>/', methods=['GET'])
def index(page=1):

    search_text = request.args.get('search_text') if request.args.get('search_text') else ''
    app = current_app._get_current_object()
    portal = g.db().query(Portal).filter_by(host=app.config['SERVER_NAME']).one()
    sub_query = Article.subquery_articles_at_portal(search_text=search_text, portal=portal)
    articles, pages, page = pagination(query=sub_query, page=page)
    division = g.db().query(PortalDivision).filter_by(portal_id=portal.id, portal_division_type_id='index').one()

    return render_template('front/bird/index.html',
                           articles={a.id:
                                     dict(list(a.get_client_side_dict().items()) +
                                          list({'main_tags': {'foo': 'one_tag'}}.items()))
                                     for a in articles},
                           portal=portal.get_client_side_dict(),
                           current_division=division.get_client_side_dict(),
                           pages=pages,
                           current_page=page,
                           page_buttons=Config.PAGINATION_BUTTONS,
                           search_text=search_text)




@front_bp.route('<string:division_name>/'
                '<string:search_text>', methods=['GET'])
@front_bp.route('<string:division_name>/<int:page>/'
                '<string:search_text>', methods=['GET'])
def division(division_name, search_text, page=1):

    app = current_app._get_current_object()
    portal = g.db().query(Portal).filter_by(host=app.config['SERVER_NAME']).one()
    search_text = search_text if not request.args.get(
        'search_text') else request.args.get('search_text')
    division = g.db().query(PortalDivision).filter_by(portal_id=portal.id, name=division_name).one()

    if division.portal_division_type_id == 'news' or division.portal_division_type_id == 'events':

        sub_query = Article.subquery_articles_at_portal(search_text=search_text,
                                                        portal_division_id=division.id)
        articles, pages, page = pagination(query=sub_query, page=page)
        return render_template('front/bird/division.html',
                               articles={a.id: a.get_client_side_dict() for
                                         a in articles},
                               current_division=division.get_client_side_dict(),
                               portal=portal.get_client_side_dict(),
                               pages=pages,
                               current_page=page,
                               page_buttons=Config.PAGINATION_BUTTONS,
                               search_text=search_text)

    elif division.portal_division_type_id == 'catalog':

        # sub_query = Article.subquery_articles_at_portal(search_text=search_text,
        # articles, pages, page = pagination(query=sub_query, page=page)

        members = {member.company_id:Company.get(member.company_id).get_client_side_dict('id,name') for member in division.portal.company_assoc}

        return render_template('front/bird/catalog.html',
                               members=members,
                               current_division=division.get_client_side_dict(),
                               portal=portal.get_client_side_dict())


# TODO OZ by OZ: portal filter, move portal filtering to decorator

@front_bp.route('details/<string:article_portal_id>')
def details(article_portal_id):
    app = current_app._get_current_object()
    portal = g.db().query(Portal).filter_by(host=app.config['SERVER_NAME']).one()
    article = ArticlePortal.get(article_portal_id)
    division = g.db().query(PortalDivision).filter_by(portal_id=portal.id, id=article.division.id).one()
    article_dict = article.to_dict('id, title,short, cr_tm, md_tm, '
                'publishing_tm, keywords, status, long, image_file_id,'
                'division.name, division.portal.id,'
                'company.name')
    article_dict['tags'] = {'foo': 'one tag', 'bar': 'second tag'}

    return render_template('front/bird/article_details.html',
                           portal=portal.get_client_side_dict(),
                           current_division=division.get_client_side_dict(),
                           article=article.to_dict('id, title,short, cr_tm, md_tm, '
                'publishing_tm, status, long, image_file_id,'
                'division.name, division.portal.id,'
                'company.name'))


@front_bp.route('_c/<string:member_company_id>/<string:member_company_name>/')
@front_bp.route('_c/<string:member_company_id>/<string:member_company_name>/<int:page>/')

def subportal(member_company_id, member_company_name, page=1):
    search_text = request.args.get('search_text') if request.args.get('search_text') else ''
    app = current_app._get_current_object()
    portal = g.db().query(Portal).filter_by(host=app.config['SERVER_NAME']).one()
    sub_query = Article.subquery_articles_at_portal(search_text=search_text, portal=portal)
    articles, pages, page = pagination(query=sub_query, page=page)
    division = g.db().query(PortalDivision).filter_by(portal_id=portal.id, portal_division_type_id='index').one()

    return render_template('front/bird/subportal.html',
                           articles={a.id: a.get_client_side_dict() for
                                     a in articles},
                           subportal = True,
                           portal=portal.get_client_side_dict(),
                           current_division=division.get_client_side_dict(),
                           selected_division_id='index',
                           pages=pages,
                           current_page=page,
                           page_buttons=Config.PAGINATION_BUTTONS,
                           search_text=search_text)
