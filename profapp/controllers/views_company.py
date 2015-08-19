from .blueprints import company_bp
from flask import render_template, request, url_for, g, redirect
from ..models.company import Company, UserCompanyRight, Right
from .request_wrapers import replace_brackets
# from phonenumbers import NumberParseException
from .errors import SubscribeToOwn


@company_bp.route('/', methods=['GET', 'POST'])
def show():

    company = Company()
    companies = company.query_all_companies(g.user_dict['id'])

    return render_template('company.html',
                           companies=companies
                           )

@company_bp.route('/add/')
def add():

    return render_template('company_add.html',
                           user=g.user_dict)

@company_bp.route('/confirm_add/', methods=['POST'])
def confirm_add():

    company = Company()
    company.create_company(data=request.form)

    return redirect(url_for('company.show'))

@company_bp.route('/profile/<string:company_id>/', methods=['GET', 'POST'])
def profile(company_id):

    company = Company()
    r = Right()
    r.show_rights(company_id)
    comp = company.query_company(company_id=company_id)
    user_rights = company.query_employee(comp_id=company_id)

    return render_template('company_profile.html',
                           comp=comp,
                           user_rights=user_rights
                           )

@company_bp.route('/employees/<string:comp_id>/', methods=['GET', 'POST'])
def employees(comp_id):

    company = Company()
    r = Right()
    company_user_rights = r.show_rights(comp_id)
    current_company = company.query_company(company_id=comp_id)

    return render_template('company_employees.html',
                           comp=current_company,
                           company_user_rights=company_user_rights
                           )

@company_bp.route('/edit/<string:company_id>/')
def edit(company_id):

    company = Company()
    comp_query = company.query_company(company_id=company_id)
    user_query = company.query_employee(comp_id=company_id)

    return render_template('company_edit.html',
                           comp=comp_query,
                           user_query=user_query
                           )

@company_bp.route('/confirm_edit/<string:company_id>', methods=['POST'])
def confirm_edit(company_id):

    company = Company()
    company.update_comp(company_id=company_id, data=request.form)
    return redirect(url_for('company.profile', company_id=company_id))

@company_bp.route('/subscribe/<string:company_id>/')
def subscribe(company_id):

    comp_role = UserCompanyRight()
    comp_role.subscribe_to_company(company_id)

    return redirect(url_for('company.profile', company_id=company_id))

@company_bp.route('/subscribe_search/', methods=['POST'])
def subscribe_search_form():

    comp_role = UserCompanyRight()
    company = Company()
    data = request.form
    if not company.query_employee(comp_id=data['company']):
        comp_role.subscribe_to_company(data['company'])
    else:
        raise SubscribeToOwn
    return redirect(url_for('company.profile', company_id=data['company']))

@company_bp.route('/add_subscriber/', methods=['POST'])
def confirm_subscriber():

    comp_role = UserCompanyRight()
    data = request.form
    comp_role.apply_request(comp_id=data['comp_id'], user_id=data['user_id'], bool=data['req'])

    return redirect(url_for('company.profile', company_id=data['comp_id']))
