from .blueprints import company_bp
from flask import render_template, request, url_for, g, redirect
from ..models.company import Company
from ..models.user_company_role import UserCompanyRole, Right
from .request_wrapers import replace_brackets
# from phonenumbers import NumberParseException
from .errors import SubscribeToOwn
company = Company()
comp_role = UserCompanyRole()
r = Right()

@company_bp.route('/', methods=['GET', 'POST'])
def show_company():

    companies = company.query_all_companies(g.user_dict['id'])

    return render_template('company.html',
                           companies=companies,
                           user=g.user_dict
                           )

@company_bp.route('/add_company/', methods=['GET', 'POST'])
def add_company():

    if request.method != 'GET':
        # We have to catch NumberParseException
        company.add_comp(data=request.form)

        return redirect(url_for('company.show_company'))

    return render_template('add_company.html',
                           id=g.user_dict['id'],
                           user=g.user_dict)

@company_bp.route('/company_profile/<string:id>/', methods=['GET', 'POST'])
def company_profile(id):

    query = company.query_company(id=id)
    non_active_subscribers = company.query_non_active(id=id)
    user_name = [x.user_name() for x in non_active_subscribers]
    user_query = company.query_subscriber_all_status(comp_id=id)
    user_active = company.query_subscriber_active_status(comp_id=id)

    return render_template('company_profile.html',
                           comp=query,
                           non_active_subscribers=non_active_subscribers,
                           user=g.user_dict,
                           user_name=user_name,
                           user_query=user_query,
                           user_active=user_active
                           )

@company_bp.route('/employees/<string:comp_id>/', methods=['GET', 'POST'])
def employees(comp_id):

    show_rights = r.show_rights(comp_id=comp_id)
    query = company.query_company(id=comp_id)
    user_query = company.query_subscriber_all_status(comp_id=comp_id)
    companies = []
    for c in show_rights:
        companies.append(company.query_all_companies(c))

    return render_template('company_employees.html',
                           rights=show_rights,
                           user=g.user_dict,
                           comp=query,
                           companies=companies,
                           user_query=user_query
                           )

@company_bp.route('/edit/<string:id>/', methods=['GET', 'POST'])
@replace_brackets
def edit(id):

    comp_query = company.query_company(id=id)
    user_query = company.query_subscriber_all_status(comp_id=id)
    if request.method != 'GET':
        # We have to catch NumberParseException
        company.update_comp(id=id, data=request.form)
        return redirect(url_for('company.company_profile', id=id))

    return render_template('company_edit.html',
                           comp=comp_query,
                           user=g.user_dict,
                           user_query=user_query
                           )

@company_bp.route('/subscribe/<string:id>/', methods=['GET', 'POST'])
def subscribe(id):

    if request.method != 'GET':
        data = request.form
        id = data['company']
    if g.user_dict['id'] != company.query_company(id=id).author_user_id:
        comp_role.subscribe_to_company(id)
    else:
        raise SubscribeToOwn

    return redirect(url_for('company.company_profile', id=id))

@company_bp.route('/add_subscriber/', methods=['GET', 'POST'])
def add_subscriber():

    data = request.form
    comp_role.apply_request(comp_id=data['comp_id'], user_id=data['user_id'], bool=data['req'])

    return redirect(url_for('company.company_profile', id=data['comp_id']))
