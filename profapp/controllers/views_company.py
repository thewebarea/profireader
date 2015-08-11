from .blueprints import company_bp
from flask import render_template, request, url_for, g, redirect
from db_init import db_session
from ..models.company import Company
from ..models.user_company_role import UserCompanyRole
from .request_wrapers import replace_brackets
# from phonenumbers import NumberParseException
from ..constants.STATUS import STATUS

@company_bp.route('/', methods=['GET', 'POST'])
def show_company():
    company = Company()
    companies = company.query_all_companies(g.user.id)

    return render_template('company.html',
                           companies=companies
                           )

@company_bp.route('/add_company/', methods=['GET', 'POST'])
def add_company():

    if request.method != 'GET':
        company = Company()
        # We have to catch NumberParseException
        company.add_comp(data=request.form)

        return redirect(url_for('company.show_company'))

    return render_template('add_company.html', id=g.user.id)

@company_bp.route('/company_profile/<string:id>/')
@replace_brackets
def company_profile(id):

    company = Company()
    query = company.query_company(id=id)
    comp_role = UserCompanyRole()
    non_active_subscribers = comp_role.query_non_active(id=id)


    return render_template('company_profile.html',
                           comp=query,
                           non_active_subscribers=non_active_subscribers
                           )

@company_bp.route('/edit/<string:id>/', methods=['GET', 'POST'])
@replace_brackets
def edit(id):

    company = Company()
    query = company.query_company(id=id)
    if request.method != 'GET':
        # We have to catch NumberParseException
        company.update_comp(id=id, data=request.form)
        return redirect(url_for('company.company_profile', id=id))

    return render_template('company_edit.html',
                           comp=query
                           )

@company_bp.route('/subscribe/', methods=['GET', 'POST'])
@replace_brackets
def subscribe():

    data = request.form
    id = data['company']
    comp_role = UserCompanyRole()
    comp_role.subscribe_to_company(id)

    return redirect(url_for('company.company_profile', id=id))

@company_bp.route('/add_subscriber/<string:user_id>/<string:comp_id>', methods=['GET', 'POST'])
@replace_brackets
def add_subscriber(user_id, comp_id):
    comp_role = UserCompanyRole()
    comp_role.apply_request(comp_id=comp_id, user_id=user_id)
    return redirect(url_for('company.company_profile', id=comp_id))