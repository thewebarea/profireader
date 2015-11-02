from .blueprints import portal_bp
from flask import render_template, g, jsonify
from ..models.company import Company
from flask.ext.login import current_user, login_required
from ..models.portal import PortalDivisionType
from utils.db_utils import db
from ..models.portal import CompanyPortal, Portal, PortalLayout, PortalDivision
from .request_wrapers import ok, check_rights
from ..models.articles import ArticlePortal, ArticleCompany
from ..models.company import simple_permissions
from ..models.rights import Right
from profapp.models.rights import RIGHTS
from ..controllers import errors
from ..models.files import File, FileContent
from .pagination import pagination
from ..constants.ARTICLE_STATUSES import ARTICLE_STATUS_IN_PORTAL
from config import Config


@portal_bp.route('/create/<string:company_id>/', methods=['GET'])
@login_required
def create_template(company_id):
    return render_template('company/portal_create.html', company_id=company_id)





@portal_bp.route('/<any(create,update):action>/<any(validate,save):state>/<string:company_id>/',
                 methods=['POST'])
@login_required
# @check_rights(simple_permissions([Right[RIGHTS.MANAGE_PORTAL()]]))
@ok
def create_save(json, action, state, company_id):
    layouts = [x.get_client_side_dict() for x in db(PortalLayout).all()]
    types = {x.id: x.get_client_side_dict() for x in
             PortalDivisionType.get_division_types()}

    # member_company = Portal.companies
    company = Company.get(company_id)
    member_companies = {company_id: company.get_client_side_dict()}
    return {'company_id': company_id,
            'portal_company_members': member_companies,
            'portal': {'company_id': company_id, 'name': '', 'host': '',
                       'logo_file_id': company.logo_file_id,
                       'portal_layout_id': layouts[0]['id'],
                       'divisions': [
                           {'name': 'index page', 'portal_division_type_id': 'index'},
                           {'name': 'news', 'portal_division_type_id': 'news'},
                           {'name': 'events', 'portal_division_type_id': 'events'},
                           {'name': 'catalog', 'portal_division_type_id': 'catalog'},
                           {'name': 'our subportal', 'portal_division_type_id': 'company_subportal',
                            'settings': {'company_id': company_id}},
                       ]},
            'layouts': layouts, 'division_types': types}


@portal_bp.route('/confirm_create/<string:company_id>/', methods=['POST'])
@login_required
# @check_rights(simple_permissions([Right[RIGHTS.MANAGE_PORTAL()]]))
@ok
def confirm_create(json, company_id):
    portal = Portal(name=json['name'], host=json['host'], portal_layout_id=json['portal_layout_id'],
                    company_owner_id=company_id).create_portal().save()

    portal.divisions = [PortalDivision(portal_id=portal.id, **division) for division in
                        json['divisions']]

    validation_result = portal.validate()

    if '__validation' in json:
        db = getattr(g, 'db', None)
        db.rollback()
        return validation_result
    elif len(validation_result['errors'].keys()):
        raise errors.ValidationException(validation_result)
    else:
        company_owner = Company.get(company_id)
        portal.logo_file_id = File.get(json['logo_file_id']).copy_file(
            company_id=company_id, root_folder_id=company_owner.system_folder_file_id,
            parent_folder_id=company_owner.system_folder_file_id,
            article_portal_id=None).save().id
        return {'company_id': company_id}

    ret = {
        'company_id': company_id,
        'layouts': layouts,
        'division_types': {x.id: x.get_client_side_dict() for x in
                           PortalDivisionType.get_division_types()}
    }

    if action == 'create':
        ret['portal'] = {'company_id': company_id, 'name': '', 'host': '',
                         'portal_layout_id': layouts[0]['id'],
                         'divisions': [
                             {'name': 'index page', 'portal_division_type_id': 'index'},
                             {'name': 'news', 'portal_division_type_id': 'news'},
                             {'name': 'events', 'portal_division_type_id': 'events'},
                             {'name': 'catalog', 'portal_division_type_id': 'catalog'},
                             {'name': 'about', 'portal_division_type_id': 'about'},
                         ]}
    else:
        ret['portal'] = {}

    return ret



@portal_bp.route('/', methods=['POST'])
@login_required
# @check_rights(simple_permissions([]))
@ok
def apply_company(json):
    CompanyPortal.apply_company_to_portal(company_id=json['company_id'],
                                          portal_id=json['portal_id'])
    return {'portals_partners': [portal.portal.to_dict(
        'name, company_owner_id,id') for portal in CompanyPortal.get_portals(json['company_id'])],
        'company_id': json['company_id']}

# TODO ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@portal_bp.route('/profile/<string:portal_id>/', methods=['GET'])
@login_required
# @check_rights(simple_permissions([]))
def profile(portal_id):
    return render_template('company/portal_profile.html')


@portal_bp.route('/profile/<string:portal_id>/', methods=['POST'])
@login_required
# @check_rights(simple_permissions([]))
@ok
def profile_load(json, portal_id):
    portal = db(Portal, id=portal_id).one()

    tags = set(tag_portal_division.tag for tag_portal_division in portal.portal_tags)
    tags_dict = {tag.id: tag.name for tag in tags}
    return {'portal': portal.to_dict('*, divisions.*, own_company.*, portal_tags.*'),
            'portal_id': portal_id,
            'tag': tags_dict}


@portal_bp.route('/partners/<string:company_id>/', methods=['GET'])
@login_required
# @check_rights(simple_permissions([]))
def partners(company_id):
    return render_template('company/company_partners.html', company_id=company_id)


@portal_bp.route('/partners/<string:company_id>/', methods=['POST'])
@login_required
# @check_rights(simple_permissions([]))
@ok
def partners_load(json, company_id):
    portal = db(Company, id=company_id).one().own_portal
    companies_partners = [comp.to_dict('id, name') for comp in
                          portal.companies] if portal else []
    portals_partners = [port.portal.to_dict('name, company_owner_id, id')
                        for port in CompanyPortal.get_portals(
                        company_id) if port]
    user_rights = list(g.user.user_rights_in_company(company_id))
    return {'portal': portal.to_dict('name') if portal else [],
            'companies_partners': companies_partners,
            'portals_partners': portals_partners,
            'company_id': company_id,
            'user_rights': user_rights}


@portal_bp.route('/search_for_portal_to_join/', methods=['POST'])
@ok
@login_required
# @check_rights(simple_permissions([]))
def search_for_portal_to_join(json):
    portals_partners = Portal.search_for_portal_to_join(
        json['company_id'], json['search'])
    return portals_partners


@portal_bp.route('/publications/<string:company_id>/', methods=['GET'])
@login_required
# @check_rights(simple_permissions([]))
def publications(company_id):
    return render_template(
        'company/portal_publications.html', company_id=company_id,
        angular_ui_bootstrap_version='//angular-ui.github.io/bootstrap/ui-bootstrap-tpls-0.14.2.js')

@portal_bp.route('/publications/<string:company_id>/', methods=['POST'])
@login_required
# @check_rights(simple_permissions([]))
@ok
def publications_load(json, company_id):
    portal = db(Company, id=company_id).one().own_portal
    if not portal:
        return dict(portal_not_exist=True)
    current_page = json.get('pages')['current_page'] if json.get('pages') else 1
    chosen_company_id = json.get('chosen_company')['id'] if json.get('chosen_company') else 0
    params = {'search_text': json.get('search_text'), 'portal_id': portal.id}
    article_status = json.get('chosen_status')
    original_chosen_status = None

    if article_status and article_status != 'All':
        params['status'] = original_chosen_status = article_status
    subquery = ArticlePortal.subquery_portal_articles(**params)
    if chosen_company_id:
        subquery = subquery.filter(db(ArticleCompany,
                                      company_id=chosen_company_id,
                                      id=ArticlePortal.article_company_id).exists())
    articles, pages, current_page = pagination(subquery,
                                               page=current_page,
                                               items_per_page=5)
    all, companies = ArticlePortal.get_companies_which_send_article_to_portal(portal.id)
    statuses = {status: status for status in ARTICLE_STATUS_IN_PORTAL.all}
    statuses['All'] = 'All'

    return {'articles': [a.get_client_side_dict() for a in articles],
            'companies': companies,
            'search_text': json.get('search_text') or '',
            'original_search_text': json.get('search_text') or '',
            'chosen_company': json.get('chosen_company') or all,
            'pages': {'total': pages,
                      'current_page': current_page,
                      'page_buttons': Config.PAGINATION_BUTTONS},
            'company_id': company_id,
            'chosen_status': article_status or statuses['All'],
            'statuses': statuses,
            'original_chosen_status': original_chosen_status,
            'user_rights': list(g.user.user_rights_in_company(company_id))}

@portal_bp.route('/publication_details/<string:article_id>/<string:company_id>', methods=['GET'])
@login_required
def publication_details(article_id, company_id):
    return render_template('company/publication_details.html',
                           company_id=company_id)

@portal_bp.route('/publication_details/<string:article_id>/<string:company_id>', methods=['POST'])
@login_required
@ok
def publication_details_load(json, article_id, company_id):
    statuses = {status: status for status in ARTICLE_STATUS_IN_PORTAL.all}
    article = db(ArticlePortal, id=article_id).one().get_client_side_dict()
    new_status = ARTICLE_STATUS_IN_PORTAL.published \
        if article['status'] != ARTICLE_STATUS_IN_PORTAL.published \
        else ARTICLE_STATUS_IN_PORTAL.declined
    return {'article': article,
            'user_rights': list(g.user.user_rights_in_company(company_id)),
            'statuses': statuses,
            'new_status': new_status}


@portal_bp.route('/update_article_portal/<string:article_id>', methods=['POST'])
@login_required
@ok
def update_article_portal(json, article_id):

    db(ArticlePortal, id=article_id).update({'status': json.get('new_status')})
    json['article']['status'] = json.get('new_status')
    json['new_status'] = ARTICLE_STATUS_IN_PORTAL.published \
        if json.get('new_status') != ARTICLE_STATUS_IN_PORTAL.published \
        else ARTICLE_STATUS_IN_PORTAL.declined
    return json
