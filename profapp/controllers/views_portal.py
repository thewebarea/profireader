from .blueprints import portal_bp
from flask import render_template, request, url_for, redirect
from ..models.company import Company
from flask.ext.login import login_required
from ..models.portal import PortalDivisionType
from utils.db_utils import db
from ..models.portal import CompanyPortal, Portal
from .request_wrapers import ok, check_rights
from ..models.articles import ArticlePortal
from ..models.company import simple_permissions
from flask import g

@portal_bp.route('/create/<string:company_id>/', methods=['GET'])
@check_rights(simple_permissions(frozenset()))
def create(company_id):
    return render_template('company/portal_create.html',
                           company_id={'id': company_id})

@portal_bp.route('/create/<string:company_id>/', methods=['POST'])
@check_rights(simple_permissions(frozenset()))
@ok
def create_load(json, company_id):

    return {'company_id': company_id, 'portal_name': '',
            'division_name': '', 'division_type': '',
            'host_name': '', 'divisions':
                [x.to_dict('id') for x in
                 PortalDivisionType.get_division_types()]}

@portal_bp.route('/confirm_create/', methods=['POST'])
@check_rights(simple_permissions(frozenset()))
@ok
def confirm_create(json):
    portal = Portal(name=json['portal_name'],
                    host=json['host_name'])
    portal.create_portal(company_id=json['company_id'],
                         division_type=json['division_type'],
                         division_name=json['division_name'])
    return {'company_id': {'id': json['company_id']}}

@portal_bp.route('/', methods=['POST'])
@check_rights(simple_permissions(frozenset()))
@ok
def apply_company(json):

    CompanyPortal.apply_company_to_portal(company_id=json['company_id'],
                                          portal_id=json['portal_id'])
    return {'portals_partners': [portal.portal.to_dict(
        'name, company_owner_id,id')for portal in CompanyPortal.
        get_portals(json['company_id'])],
        'company_id': {'id': json['company_id']}}

@portal_bp.route('/partners/<string:company_id>/')
@check_rights(simple_permissions(frozenset()))
def partners(company_id):

    return render_template('company/company_partners.html',
                           company_id={'id': company_id}
                           )

@portal_bp.route('/partners/<string:company_id>/', methods=['POST'])
@check_rights(simple_permissions(frozenset()))
@ok
def partners_load(json, company_id):

    portal = Portal.own_portal(company_id)
    portal = portal.to_dict('name') if portal else []
    companies_partners = [comp.to_dict('id, name') for comp in
                          CompanyPortal.show_companies_on_my_portal(
                              company_id)]
    portals_partners = [portal.portal.to_dict('name, company_owner_id,'
                                              'id')
                        for portal in CompanyPortal.get_portals(
                        company_id)]
    return {'portal': portal, 'companies_partners': companies_partners,
            'portals_partners': portals_partners,
            'company_id': {'id': company_id}}



@portal_bp.route('/search_for_portal_to_join/', methods=['POST'])
@check_rights(simple_permissions(frozenset()))
@ok
def search_for_portal_to_join(json):
    portals_partners = Portal.search_for_portal_to_join(
        json['company_id'], json['search'])
    return portals_partners

@portal_bp.route('/publications/<string:company_id>/', methods=['GET'])
@check_rights(simple_permissions(frozenset()))
def publications(company_id):

    comp = Company().query_company(company_id=company_id)
    return render_template('company/portal_publications.html',
                           company_id={'id': company_id})

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
            'company_id': {'id': company_id}}

@portal_bp.route('/update_article_portal/', methods=['POST'])
@ok
def update_article_portal(json):

    update = json['new_status'].split('/')
    ArticlePortal.update_article_portal(update[0], **{'status':
                                                      update[1]})
    return json
