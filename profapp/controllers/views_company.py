from .blueprints import company_bp
from flask import render_template, request, url_for, g, redirect, jsonify, \
    abort
from ..models.company import Company, Right, UserCompany
from ..models.company import simple_permissions
from .request_wrapers import json, check_rights
from ..constants.STATUS import STATUS
from flask.ext.login import login_required, current_user
from utils.db_utils import db
from .request_wrapers import can_global


@company_bp.route('/trash/<string:company_id>/')
def trash(company_id):
    user = current_user

    company_query = db(Company, id=company_id)
    company_query.update({'name': 'Testing Company. Yahoo!'})

    return jsonify({'user': user.id, 'company_id': company_query.first().id})


@company_bp.route('/search_to_submit_article/', methods=['POST'])
@json
def search_to_submit_article(json):
    companies = Company().search_for_company(g.user_dict['id'], json['search'])
    return companies


@company_bp.route('/', methods=['GET', 'POST'])
@check_rights(simple_permissions(frozenset()))
@login_required
def show():
    companies = current_user.employers
    return render_template('company.html', companies=companies)


@company_bp.route('/add/')
@check_rights(simple_permissions(frozenset()))
@login_required
def add():
    return render_template('company_add.html', user=g.user_dict)


@company_bp.route('/confirm_add/', methods=['POST'])
@check_rights(simple_permissions(frozenset()))
@login_required
def confirm_add():
    data = request.form
    comp_dict = {}
    for x, y in zip(data.keys(), data.values()):
        comp_dict[x] = y
    comp_dict['passed_file'] = request.files['logo_file']
    Company(**comp_dict)

    return redirect(url_for('company.show'))


# what permissions have to be used here?
@company_bp.route('/profile/<string:company_id>/', methods=['GET', 'POST'])
@check_rights(simple_permissions(frozenset()))
@login_required
def profile(company_id):
    company = db(Company, id=company_id).one()
    user_rights_int = \
        current_user.\
        employer_assoc.\
        filter_by(company_id=company_id).\
        one().\
        rights

    user_rights_list = list(Right.transform_rights_into_set(user_rights_int))

    if company.logo_file:
        image = url_for('filemanager.get', id=company.logo_file)
    else:
        image = ''

    return render_template('company_profile.html',
                           comp=company,
                           user_rights=user_rights_list,
                           image=image
                           )


@company_bp.route('/employees/<string:comp_id>/')
@check_rights(simple_permissions(frozenset()))
@login_required
def employees(comp_id):
    company_user_rights = UserCompany.show_rights(comp_id)
    curr_user = {g.user_dict['id']: company_user_rights[user] for user
                 in company_user_rights if user == g.user_dict['id']}
    current_company = db(Company, id=comp_id).one()

    return render_template('company_employees.html',
                           comp=current_company,
                           company_user_rights=company_user_rights,
                           curr_user=curr_user
                           )


@company_bp.route('/update_rights', methods=['POST'])
@check_rights(simple_permissions(
              frozenset(['manage_access_company']))
              )
@login_required
def update_rights():
    data = request.form
    UserCompany.update_rights(user_id=data['user_id'],
                              comp_id=data['comp_id'],
                              new_rights=data.getlist('right')
                              )

    return redirect(url_for('company.employees', comp_id=data['comp_id']))


# must be corrected
@company_bp.route('/edit/<string:company_id>/')
@check_rights(simple_permissions(
              frozenset(['manage_access_company', 'edit']))
              )
@login_required
def edit(company_id):
    # todo: it must be checked!!!
    company = db(Company, id=company_id).one()

    user = current_user
    # user = Company().query_employee(comp_id=company_id)

    # rights_lambda_rule = simple_permissions(frozenset('edit'))
    # if not can_global(rights_lambda_rule,
    #                   user=current_user,
    #                   company_id=company_id):
    #     abort(403)
    return render_template('company_edit.html', comp=company, user_query=user)


@company_bp.route('/confirm_edit/<string:company_id>', methods=['POST'])
@check_rights(simple_permissions(
              frozenset(['add_employee']))
              )
@login_required
def confirm_edit(company_id):
    Company().update_comp(company_id=company_id, data=request.form,
                          passed_file=request.files['logo_file'])
    return redirect(url_for('company.profile', company_id=company_id))


@company_bp.route('/subscribe/<string:company_id>/')
@check_rights(simple_permissions(frozenset()))
@login_required
def subscribe(company_id):
    comp_role = UserCompany(user_id=g.user_dict['id'], company_id=company_id,
                            status=STATUS().NONACTIVE())
    comp_role.subscribe_to_company()

    return redirect(url_for('company.profile', company_id=company_id))


@company_bp.route('/subscribe_search/', methods=['POST'])
@check_rights(simple_permissions(frozenset()))
@login_required
def subscribe_search_form():
    data = request.form
    comp_role = UserCompany(user_id=g.user_dict['id'],
                            company_id=data['company'],
                            status=STATUS().NONACTIVE())
    comp_role.subscribe_to_company()

    return redirect(url_for('company.profile', company_id=data['company']))


@company_bp.route('/add_subscriber/', methods=['POST'])
@check_rights(simple_permissions(frozenset(['add_employee'])))
@login_required
def confirm_subscriber():
    comp_role = UserCompany()
    data = request.form
    comp_role.apply_request(comp_id=data['comp_id'], user_id=data['user_id'],
                            bool=data['req'])

    return redirect(url_for('company.profile', company_id=data['comp_id']))


@company_bp.route('/suspend_employee/', methods=['POST'])
@check_rights(simple_permissions(frozenset(['suspend_employee'])))
@login_required
def suspend_employee():
    data = request.form
    UserCompany.suspend_employee(user_id=data['user_id'],
                                 comp_id=data['comp_id'])
    return redirect(url_for('company.employees', comp_id=data['comp_id']))


@company_bp.route('/suspended_employees/<string:comp_id>')
@check_rights(simple_permissions(frozenset()))
@login_required
def suspended_employees_func(comp_id):
    comp = Company().query_company(company_id=comp_id)
    suspended_employees = \
        UserCompany.suspend_employee(comp_id, user_id=current_user.get_id())
    return render_template('company_suspended.html',
                           suspended_employees=suspended_employees,
                           comp=comp
                           )
