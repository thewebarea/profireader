from .blueprints import portal_bp
from flask import render_template, request, url_for, redirect
from ..models.company import Company
from flask.ext.login import login_required
from ..models.portal import CompanyPortal, Portal
from .request_wrapers import ok

@portal_bp.route('/', methods=['POST'])
@login_required
def apply_company():

    data = request.form
    CompanyPortal.apply_company_to_portal(company_id=data['comp_id'],
                                          portal_id=data['portal_id'])
    return redirect(url_for('portal.partners',
                            company_id=data['comp_id']))

@portal_bp.route('/partners/<string:company_id>/')
@login_required
def partners(company_id):

    comp = Company().query_company(company_id=company_id)
    companies_partners = CompanyPortal().\
        show_companies_on_my_portal(company_id)
    portals_partners = CompanyPortal().show_portals(company_id)

    return render_template('company/company_partners.html',
                           comp=comp,
                           companies_partners=companies_partners,
                           portals_partners=portals_partners
                           )

@portal_bp.route('/publications/<string:company_id>/', methods=['GET'])
def publications(company_id):

    comp = Company().query_company(company_id=company_id)
    return render_template('company/portal_publications.html',
                           comp=comp)

@portal_bp.route('/publications/<string:company_id>/', methods=['POST'])
@ok
def publications_load(json, company_id):
    portal = Portal.own_portal(company_id)
    if portal:
        if not portal.portal_division[0]:
            return {'portal_division': [{'name': '',
                                        'article_portal': []}]}
        portal = [port.to_dict('name|id|portal_id,article_portal.'
                           'status|md_tm|cr_tm|title|long|short|id,'
                           'article_portal.company_article.company.id|'
                           'name|short_description|email|phone') for
              port in portal.portal_division if port.article_portal]

    return portal

@portal_bp.route('/update_article_portal/', methods=['POST'])
@ok
def update_article_portal(json):
    print(json['article_portal']['id'])
    return json