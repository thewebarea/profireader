from .blueprints import company_bp
from flask import render_template, request, url_for, g, redirect
from ..models.company import Company
from ..models.user_company_role import UserCompanyRight, Right
from .request_wrapers import replace_brackets
# from phonenumbers import NumberParseException
from .errors import SubscribeToOwn


@company_bp.route('/', methods=['GET', 'POST'])
def show():

    company = Company()
    companies = company.query_all_companies(g.user_dict['id'])

    return render_template('company.html',
                           companies=companies,
                           user=g.user_dict)

@company_bp.route('/add/', methods=['GET', 'POST'])
def add():

    company = Company()
    if request.method != 'GET':
        # We have to catch NumberParseException
        company.create_company(data=request.form)

        return redirect(url_for('company.show'))

    return render_template('add_company.html',
                           id=g.user_dict['id'],
                           user=g.user_dict)

@company_bp.route('/profile/<string:company_id>/', methods=['GET', 'POST'])
def profile(company_id):

    company = Company()
    comp = company.query_company(company_id=company_id)
    user_rights = company.query_employee(comp_id=company_id)

    return render_template('company_profile.html',
                           comp=comp,
                           user=g.user_dict,
                           user_rights=user_rights
                           )

@company_bp.route('/employees/<string:comp_id>/', methods=['GET', 'POST'])
def employees(comp_id):

    r = Right()
    company = Company()
    non_active_subscribers = company.query_non_active(company_id=comp_id)
    user_name = [x.user_name() for x in non_active_subscribers]
    show_rights = r.show_rights(comp_id=comp_id)
    query = company.query_company(company_id=comp_id)
    companies = []
    user_query = company.query_employee(comp_id=comp_id)
    for c in show_rights:
        companies.append(company.query_all_companies(c))

    return render_template('company_employees.html',
                           rights=show_rights,
                           user=g.user_dict,
                           comp=query,
                           companies=companies,
                           user_query=user_query,
                           user_name=user_name,
                           non_active_subscribers=non_active_subscribers
                           )

@company_bp.route('/edit/<string:company_id>/', methods=['GET', 'POST'])
@replace_brackets
def edit(company_id):

    company = Company()
    comp_query = company.query_company(company_id=company_id)
    user_query = company.query_employee(comp_id=company_id)
    if request.method != 'GET':
        # We have to catch NumberParseException
        company.update_comp(company_id=company_id, data=request.form)
        return redirect(url_for('company.profile', company_id=company_id))

    return render_template('company_edit.html',
                           comp=comp_query,
                           user=g.user_dict,
                           user_query=user_query
                           )

@company_bp.route('/subscribe/<string:company_id>/', methods=['GET', 'POST'])
def subscribe(company_id):

    comp_role = UserCompanyRight()
    company = Company()
    if request.method != 'GET':
        data = request.form
        company_id = data['company']
    if g.user_dict['id'] != company.query_company(company_id=company_id).author_user_id:
        comp_role.subscribe_to_company(company_id)
    else:
        raise SubscribeToOwn

    return redirect(url_for('company.profile', company_id=company_id))

@company_bp.route('/add_subscriber/', methods=['GET', 'POST'])
def confirm_subscriber():

    comp_role = UserCompanyRight()
    data = request.form
    comp_role.apply_request(comp_id=data['comp_id'], user_id=data['user_id'], bool=data['req'])

    return redirect(url_for('company.profile', company_id=data['comp_id']))
