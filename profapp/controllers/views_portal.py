from .blueprints import portal_bp
from flask import render_template, request, url_for, g, redirect
from ..models.company import Company, UserCompanyRight, Right
# from phonenumbers import NumberParseException
from .errors import SubscribeToOwn
from .has_right import has_right
from ..constants.USER_ROLES import RIGHTS
from ..models.portal import CompanyPortal

@portal_bp.route('/', methods=['POST'])
def apply_company():

    data = request.form
    CompanyPortal.apply_company_to_portal(company_id=data['comp_id'], portal_id=data['portal_id'])
    return redirect(url_for('portal.partners', company_id=data['comp_id']))

@portal_bp.route('/partners/<string:company_id>/')
def partners(company_id):

    comp = Company().query_company(company_id=company_id)
    companies_partners = CompanyPortal.show_companies_on_portal(company_id)
    return render_template('company_partners.html',
                           comp=comp,
                           companies_partners=companies_partners
                           )
