from .blueprints import portal_bp
from flask import render_template, request, url_for, redirect
from ..models.company import Company
from flask.ext.login import login_required
from ..models.portal import CompanyPortal, Portal
from .request_wrapers import ok
from ..models.articles import ArticlePortal

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
        if not portal.divisions[0]:
            return {'divisions': [{'name': '',
                                   'article_portal': []}]}
        portal = [port.to_dict('name|id|portal_id,article_portal.'
                           'status|md_tm|cr_tm|title|long|short|id,'
                           'article_portal.company_article.company.id|'
                           'name|short_description|email|phone') for
                  port in portal.divisions if port.article_portal]

    return {'portal': portal, 'new_status': ''}

@portal_bp.route('/update_article_portal/', methods=['POST'])
@ok
def update_article_portal(json):

    update = json['new_status'].split('/')
    ArticlePortal.update_article_portal(update[0], **{'status':
                                                      update[1]})
    return json
