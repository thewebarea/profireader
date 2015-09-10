from .blueprints import portal_bp
from flask import render_template, request, url_for, redirect
from ..models.company import Company
from flask.ext.login import login_required
from ..models.portal import PortalDivisionType
from utils.db_utils import db
from ..models.portal import CompanyPortal, Portal, PortalLayout, PortalDivision
from .request_wrapers import ok, check_rights
from ..models.articles import ArticlePortal
from ..models.company import simple_permissions
from flask import g


@portal_bp.route('/create/<string:company_id>/', methods=['GET'])
@check_rights(simple_permissions([]))
def create(company_id):
    return render_template('company/portal_create.html',
                           company_id=company_id)


@portal_bp.route('/create/<string:company_id>/', methods=['POST'])
@check_rights(simple_permissions([]))
@ok
def create_load(json, company_id):
    layouts = [x.get_client_side_dict() for x in db(PortalLayout).all()]
    types = [x.get_client_side_dict() for x in
             PortalDivisionType.get_division_types()]

    return {'company_id': company_id,
            'portal': {'company_id': company_id, 'name': '', 'host': '',
                       'portal_layout_id': layouts[0]['id'],
                       'divisions': [
                           {'name': 'some news', 'portal_division_type_id': 'news'}]},
            'layouts': layouts, 'division_types': types}


@portal_bp.route('/confirm_create/<string:company_id>/', methods=['POST'])
@check_rights(simple_permissions([]))
@ok
def confirm_create(json, company_id):
    portal = Portal(name=json['name'], host=json['host'],
                    portal_layout_id=json['portal_layout_id'],
                    company_owner_id=company_id,
                    divisions=[PortalDivision(**division)
                               for division in json['divisions']])
    portal_id = portal.create_portal().id
    return {'company_id': company_id, 'portal_id': portal_id}


@portal_bp.route('/', methods=['POST'])
@check_rights(simple_permissions([]))
@ok
def apply_company(json):
    CompanyPortal.apply_company_to_portal(company_id=json['company_id'],
                                          portal_id=json['portal_id'])
    return {'portals_partners': [portal.portal.to_dict(
        'name, company_owner_id,id') for portal in CompanyPortal.
                                     get_portals(json['company_id'])],
            'company_id': json['company_id']}


@portal_bp.route('/partners/<string:company_id>/')
@check_rights(simple_permissions([]))
def partners(company_id):
    return render_template('company/company_partners.html',
                           company_id=company_id
                           )


@portal_bp.route('/partners/<string:company_id>/', methods=['POST'])
@check_rights(simple_permissions([]))
@ok
def partners_load(json, company_id):

    portal = Portal.own_portal(company_id)
    companies_partners = [comp.to_dict('id, name') for comp in
                          portal.companies] if portal else []
    portals_partners = [port.portal.to_dict('name, company_owner_id, id')
                        for port in CompanyPortal.get_portals(
                        company_id) if port]
    return {'portal': portal.to_dict('name') if portal else [],
            'companies_partners': companies_partners,
            'portals_partners': portals_partners,
            'company_id': company_id}


@portal_bp.route('/search_for_portal_to_join/', methods=['POST'])
@check_rights(simple_permissions([]))
@ok
def search_for_portal_to_join(json):
    portals_partners = Portal.search_for_portal_to_join(
        json['company_id'], json['search'])
    return portals_partners


@portal_bp.route('/publications/<string:company_id>/', methods=['GET'])
@check_rights(simple_permissions([]))
def publications(company_id):
    comp = Company().query_company(company_id=company_id)
    return render_template('company/portal_publications.html',
                           company_id=company_id)


@portal_bp.route('/publications/<string:company_id>/', methods=['POST'])
@ok
def publications_load(json, company_id):
    portal = Portal.own_portal(company_id)
    if portal:
        if not portal.divisions[0]:
            return {'divisions': [{'name': '',
                                   'article_portal': []}]}
        portal = [port.to_dict('name|id|portal_id,article_portal.'
                               'status|md_tm|cr_tm|title|long|short|id,'
                               'article_portal.'
                               'company_article.company.id|'
                               'name|short_description|email|phone') for
                  port in portal.divisions if port.article_portal]

    return {'portal': portal, 'new_status': '',
            'company_id': company_id}


@portal_bp.route('/update_article_portal/', methods=['POST'])
@ok
def update_article_portal(json):
    update = json['new_status'].split('/')
    ArticlePortal.update_article_portal(update[0], **{'status': update[1]})
    return json
