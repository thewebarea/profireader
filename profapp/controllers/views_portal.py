from .blueprints import portal_bp
from flask import render_template, request, url_for, redirect
from ..models.company import Company
from flask.ext.login import login_required
from ..models.portal import CompanyPortal
from utils.db_utils import db

@portal_bp.route('/', methods=['POST'])
@login_required
def apply_company():

    data = request.form
    CompanyPortal.apply_company_to_portal(company_id=data['comp_id'],
                                          portal_id=data['portal_id'])
    return redirect(url_for('portal.partners', company_id=data['comp_id']))

@portal_bp.route('/partners/<string:company_id>/')
@login_required
def partners(company_id):
    comp = db(Company, id=company_id).one()
    companies_partners = CompanyPortal().\
        show_companies_on_my_portal(company_id)
    portals_partners = CompanyPortal().show_my_portals(company_id)

    return render_template('company_partners.html',
                           comp=comp,
                           companies_partners=companies_partners,
                           portals_partners=portals_partners
                           )
