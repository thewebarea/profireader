from .blueprints import portal_bp
from flask import render_template, g, flash, redirect, url_for, jsonify
from ..models.company import Company
from flask.ext.login import current_user, login_required
from ..models.portal import PortalDivisionType
from utils.db_utils import db
from ..models.portal import CompanyPortal, Portal, PortalLayout, PortalDivision
from ..models.tag import Tag, TagPortalDivision
from .request_wrapers import ok, check_rights
from ..models.articles import ArticlePortal
from ..models.company import simple_permissions
from ..models.rights import Right
from profapp.models.rights import RIGHTS
from ..controllers import errors
from ..models.files import File, FileContent
import copy


@portal_bp.route('/create/<string:company_id>/', methods=['GET'])
@login_required
# @check_rights(simple_permissions([]))
def create(company_id):
    return render_template('company/portal_create.html',
                           company_id=company_id)


@portal_bp.route('/create/<string:company_id>/', methods=['POST'])
@login_required
# @check_rights(simple_permissions([Right[RIGHTS.MANAGE_PORTAL()]]))
@ok
def create_load(json, company_id):
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
        portal.logo_file_id = \
            File.get(json['logo_file_id']).\
            copy_file(company_id=company_id,
                      root_folder_id=company_owner.system_folder_file_id,
                      parent_folder_id=company_owner.system_folder_file_id,
                      article_portal_id=None).save().id
        return {'company_id': company_id}


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


@portal_bp.route('/profile/<string:portal_id>/', methods=['GET'])
@login_required
# @check_rights(simple_permissions([]))
def profile(portal_id):
    company_id = db(Portal, id=portal_id).one().company_owner_id
    return render_template('company/portal_profile.html', company_id=company_id)


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


@portal_bp.route('/profile_edit/<string:portal_id>/', methods=['GET'])
@login_required
# @check_rights(simple_permissions([]))
def profile_edit(portal_id):
    company_id = db(Portal, id=portal_id).one().company_owner_id
    return render_template('company/portal_profile_edit.html', company_id=company_id)


@portal_bp.route('/profile_edit/<string:portal_id>/', methods=['POST'])
@login_required
# @check_rights(simple_permissions([]))
@ok
def profile_edit_load(json, portal_id):
    portal = db(Portal, id=portal_id).one()

    if 'profile_tags_edit' in json.keys():  # here all changes with tags in db will be done
        def strip_new_tags(json):
            """ Strips tags have gotten from input prameter json
            :param json: {'bound_tags' [{'portal_division_id': '....', 'tag_name': '  sun  '}, ...],
                'notbound_tags': [{'portal_division_id': '....', 'tag_name': '  moon  '}, ...], 'confirm_profile_edit': True}
            :return:     {'bound_tags' [{'portal_division_id': '....', 'tag_name': 'sun'}, ...],
                'notbound_tags': [{'portal_division_id': '....', 'tag_name': 'moon'}, ...], 'confirm_profile_edit': True}
            I guess this function is redundant as client does't allow to add tag with trailed blanks.
            """

            def stripping(json_new_value):
                new_list = []
                for elem in json_new_value:
                    new_elem = copy.deepcopy(elem)
                    new_elem['tag_name'] = new_elem['tag_name'].strip()
                    new_list.append(new_elem)
                return new_list

            json_new = {'bound_tags': [], 'notbound_tags': []}

            key = 'bound_tags'
            json_new[key] = stripping(json[key])

            key = 'notbound_tags'
            json_new[key] = stripping(json[key])

            return json_new

        json_new = strip_new_tags(json)

        current_bound_portal_tags = portal.portal_tags

        new_bound_tags = json_new['bound_tags']  # we should add new tags and delete unnecessary tags in Tag table
        new_bound_tag_names = set(map(lambda x: x['tag_name'], new_bound_tags))

        current_bound_tags = set(map(lambda x: getattr(getattr(x, 'tag'), 'name'),
                               current_bound_portal_tags))

        deleted_bound_tags = current_bound_tags - new_bound_tag_names
        added_bound_tags = new_bound_tag_names - (new_bound_tag_names & current_bound_tags)

        actually_deleted_bound_tags = set()
        for tag_name in deleted_bound_tags:
            # x = g.db.query(Portal.id).join(Portal.portal_tags).\
            #     filter(TagPortalDivision.id=='aa')
            # y = x.all()

            portal = g.db.query(Portal.id).filter(Portal.id!=portal_id).\
                join(PortalDivision).\
                join(TagPortalDivision).\
                join(Tag).\
                filter(Tag.name==tag_name).first()

            # if portal is None:
            if not portal:
                actually_deleted_bound_tags.add(tag_name)

        # TODO (AA to AA): Now we have to check whether actually_deleted_bound_tags
        # TODO contains entirely deleted tags

        # tag0_name = current_bound_portal_tags[0].tag.name
        # y = list(current_bound_portal_tags)         # Operations with portal_tags...
        flash('Portal tags successfully updated')


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
    return render_template('company/portal_publications.html', company_id=company_id)


@portal_bp.route('/publications/<string:company_id>/', methods=['POST'])
@login_required
# @check_rights(simple_permissions([]))
@ok
def publications_load(json, company_id):
    portal = db(Company, id=company_id).one().own_portal
    if portal:
        if not portal.divisions[0]:
            return {'divisions': [{'name': '',
                                   'article_portal': []}]}
        portal = [port.to_dict('name|id|portal_id,article_portal.'
                               'status|md_tm|cr_tm|title|long|short|id,'
                               'article_portal.'
                               'company_article.company.id|'
                               'name|short_description|email|phone') for
                  port in portal.divisions if port.article_portal]

    user_rights = list(g.user.user_rights_in_company(company_id))

    return {'portal': portal, 'new_status': '',
            'company_id': company_id, 'user_rights': user_rights}


@portal_bp.route('/update_article_portal/', methods=['POST'])
@login_required
# @check_rights(simple_permissions([]))
@ok
def update_article_portal(json):
    update = json['new_status'].split('/')
    ArticlePortal.update_article_portal(update[0], **{'status': update[1]})
    return json
