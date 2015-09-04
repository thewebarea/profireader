from .blueprints import company_bp
from flask import render_template, request, url_for, g, redirect
from ..models.company import Company, UserCompanyRight, Right, \
    UserCompany
# from phonenumbers import NumberParseException
from ..constants.USER_ROLES import RIGHTS
from ..models.users import User
from .request_wrapers import ok, check_rights
from .has_right import has_right
from ..constants.STATUS import STATUS
from flask.ext.login import login_required
from ..models.articles import Article
from ..constants.ARTICLE_STATUSES import ARTICLE_STATUS_IN_COMPANY
from ..models.portal import CompanyPortal
from ..models.articles import ArticleCompany
from utils.db_utils import db

@company_bp.route('/', methods=['GET', 'POST'])
@check_rights(**Right.p(''))
@login_required
def show():
    companies = User.user_query(g.user_dict['id']).employer

    return render_template('company/company.html',
                           companies=companies
                           )

@company_bp.route('/materials/<string:company_id>/', methods=['GET'])
@check_rights(**Right.p(''))
@login_required
def materials(company_id):

    return render_template('company/materials.html',
                           comp=Company.get(company_id).
                           get_client_side_dict(),
                           articles=[art.to_dict(
                               'id, title')
                               for art in Article.
                               get_articles_submitted_to_company(
                               company_id)])

@company_bp.route('/materials/<string:company_id>/<string:article_id>/',
                  methods=['GET'])
@check_rights(**Right.p(''))
@login_required
def material_details(company_id, article_id):

    return render_template('company/material_details.html',
                           comp=Company.get(company_id).
                           get_client_side_dict()
                           )

@company_bp.route('/materials/<string:company_id>/<string:article_id>/',
                  methods=['POST'])
@ok
def load_material_details(json, company_id, article_id):
    article = Article.get_one_article(article_id).\
        to_dict('id, title,short, cr_tm, md_tm, '
                'company_id, status, long,'
                'editor_user_id, company.name,'
                'portal_article.portal_division.portal.id')
    portals = [port.to_dict('id, name, portal_division.name|id')
               for port in CompanyPortal.show_portals(company_id)
               if port]
    if article['portal_article']['portal_division']:
        portals = [port for port in portals if port['id'] !=
                   article['portal_article']['portal_division']['portal']['id']]

    status = ARTICLE_STATUS_IN_COMPANY.can_user_change_status_to(
        article['status'])

    return {'article': article, 'status': status, 'portals':
            portals, 'comp': Company.get(company_id).
            to_dict('id, employee.id|profireader_name'),
            'selected_portal': {}, 'selected_division': {}}


@company_bp.route('/update_article/', methods=['POST'])
@login_required
@ok
def update_article(json):

    ArticleCompany.update_article(
        company_id=json['comp']['id'], article_id=json['article']['id'],
        **{'status': json['article']['status']})
    return json

@company_bp.route('/submit_to_portal/', methods=['POST'])
@login_required
@ok
def submit_to_portal(json):

    article = ArticleCompany.get(json['article']['id'])
    article.clone_for_portal(json['selected_division'])
    return json

@company_bp.route('/add/')
@check_rights(**Right.p(''))
@login_required
def add():
    return render_template('company/company_add.html',
                           user=g.user_dict)


@company_bp.route('/confirm_add/', methods=['POST'])
@check_rights(**Right.p(''))
@login_required
def confirm_add():

    data = request.form
    comp_dict = {'author_user_id': g.user_dict['id']}
    for x, y in zip(data.keys(), data.values()):
        comp_dict[x] = y
    company = Company(**comp_dict)
    company.create_company(passed_file=request.files['logo_file'])

    return redirect(url_for('company.show'))


@company_bp.route('/profile/<string:company_id>/')
@check_rights(**Right.p(''))
@login_required
def profile(company_id):
    comp = Company().query_company(company_id=company_id)
    user_rights = Company().query_employee(comp_id=company_id)
    image = url_for('filemanager.get', file_id=comp.logo_file) if \
        comp.logo_file else ''

    return render_template('company/company_profile.html',
                           comp=comp,
                           user_rights=user_rights,
                           image=image
                           )


@company_bp.route('/employees/<string:comp_id>/')
@check_rights(**Right.p(''))
@login_required
def employees(comp_id):

    company = Company()
    company_user_rights = Right().show_rights(comp_id)
    curr_user = {g.user_dict['id']: company_user_rights[user] for user
                 in company_user_rights if user == g.user_dict['id']}

    current_company = company.query_company(company_id=comp_id)

    return render_template('company/company_employees.html',
                           comp=current_company,
                           company_user_rights=company_user_rights,
                           curr_user=curr_user
                           )


@company_bp.route('/update_rights', methods=['POST'])
@check_rights(**Right.p(RIGHTS.MANAGE_ACCESS_COMPANY()))
@login_required
def update_rights():
    data = request.form
    Right.update_rights(user_id=data['user_id'],
                        comp_id=data['comp_id'],
                        rights=data.getlist('right'))

    return redirect(url_for('company.employees',
                            comp_id=data['comp_id']))


@company_bp.route('/edit/<string:company_id>/')
@check_rights(**Right.p(RIGHTS.MANAGE_ACCESS_COMPANY()))
@login_required
def edit(company_id):
    comp = Company().query_company(company_id=company_id)
    user = Company().query_employee(comp_id=company_id)
    has_right(Right.permissions(g.user_dict['id'], company_id,
                                rights=[RIGHTS.EDIT()]))

    return render_template('company/company_edit.html',
                           comp=comp,
                           user_query=user
                           )


@company_bp.route('/confirm_edit/<string:company_id>', methods=['POST'])
@check_rights(**Right.p(RIGHTS.ADD_EMPLOYEE()))
@login_required
def confirm_edit(company_id):
    Company().update_comp(company_id=company_id, data=request.form,
                          passed_file=request.files['logo_file'])
    return redirect(url_for('company.profile', company_id=company_id))


@company_bp.route('/subscribe/<string:company_id>/')
@check_rights(**Right.p(''))
@login_required
def subscribe(company_id):
    comp_role = UserCompany(user_id=g.user_dict['id'],
                            company_id=company_id,
                            status=STATUS().NONACTIVE())
    comp_role.subscribe_to_company()

    return redirect(url_for('company.profile', company_id=company_id))


@company_bp.route('/subscribe_search/', methods=['POST'])
@check_rights(**Right.p(''))
@login_required
def subscribe_search_form():
    data = request.form
    comp_role = UserCompany(user_id=g.user_dict['id'],
                            company_id=data['company'],
                            status=STATUS().NONACTIVE())
    comp_role.subscribe_to_company()

    return redirect(url_for('company.profile',
                            company_id=data['company']))


@company_bp.route('/add_subscriber/', methods=['POST'])
@check_rights(**Right.p(RIGHTS.ADD_EMPLOYEE()))
@login_required
def confirm_subscriber():
    comp_role = UserCompanyRight()
    data = request.form
    comp_role.apply_request(comp_id=data['comp_id'],
                            user_id=data['user_id'], bool=data['req'])

    return redirect(url_for('company.profile',
                            company_id=data['comp_id']))


@company_bp.route('/suspend_employee/', methods=['POST'])
@check_rights(**Right.p(RIGHTS.SUSPEND_EMPLOYEE()))
@login_required
def suspend_employee():
    data = request.form
    UserCompanyRight.suspend_employee(user_id=data['user_id'],
                                      comp_id=data['comp_id'])

    return redirect(url_for('company.employees',
                            comp_id=data['comp_id']))


@company_bp.route('/suspended_employees/<string:comp_id>')
@check_rights(**Right.p(''))
@login_required
def suspended_employees(comp_id):
    comp = Company().query_company(company_id=comp_id)
    suspended_employee = Right.suspended_employees(comp_id)
    return render_template('company/company_suspended.html',
                           suspended_employees=suspended_employee,
                           comp=comp)
