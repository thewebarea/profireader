from ..constants.TABLE_TYPES import TABLE_TYPES
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from ..controllers import errors
from flask import g
from utils.db_utils import db
from .company import Company
from .pr_base import PRBase, Base
import re
import itertools
from sqlalchemy import orm
import itertools


class Portal(Base, PRBase):
    __tablename__ = 'portal'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False,
                primary_key=True)
    name = Column(TABLE_TYPES['name'])
    host = Column(TABLE_TYPES['short_name'])
    company_owner_id = Column(TABLE_TYPES['id_profireader'],
                              ForeignKey('company.id'),
                              unique=True)
    portal_plan_id = Column(TABLE_TYPES['id_profireader'],
                            ForeignKey('portal_plan.id'))

    portal_layout_id = Column(TABLE_TYPES['id_profireader'],
                              ForeignKey('portal_layout.id'))

    logo_file_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('file.id'))

    layout = relationship('PortalLayout')
    divisions = relationship('PortalDivision',
                             backref='portal',
                             order_by='desc(PortalDivision.position)',
                             primaryjoin='Portal.id==PortalDivision.portal_id')
    article = relationship('ArticlePortal', backref='portal', uselist=False)

    # companies = relationship('Company', secondary='company_portal')

    def __init__(self, name=None,
                 portal_plan_id=None,
                 company_owner_id=None, article=None,
                 host=None, divisions=[],
                 portal_layout_id=None
                 ):
        self.name = name
        self.company_owner_id = company_owner_id
        self.article = article
        self.host = host
        self.portal_layout_id = portal_layout_id
        self.divisions = divisions
        self.portal_plan_id = portal_plan_id if portal_plan_id else db(PortalPlan).first().id
        self.portal_layout_id = portal_layout_id if portal_layout_id \
            else db(PortalLayout).first().id

    def create_portal(self):
        """This method create portal in db. Before define this method you have to create
        instance of class with parameters: name, host, portal_layout_id, company_owner_id,
        divisions. Return portal)"""

        # except errors.PortalAlreadyExist as e:
        #     details = e.args[0]
        #     print(details['message'])
        self.own_company = db(Company, id=self.company_owner_id).one()
        company_assoc = CompanyPortal(company_portal_plan_id=self.portal_plan_id)
        company_assoc.portal = self
        company_assoc.company = self.own_company
        return self

    def validate(self):
        ret = {'errors': {}, 'warnings': {}, 'notices': {}}
        if db(Portal, company_owner_id=self.company_owner_id).filter(Portal.id != self.id).count():
            ret['errors']['ok'] = 'portal for company already exists'
        if not re.match('[^\s]{3,}', self.name):
            ret['errors']['name'] = 'pls enter a bit longer name'
        if not re.match(
                '^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)+([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9]{1,})$',
                self.host):
            ret['errors']['host'] = 'pls enter valid host name'
        if not 'host' in ret['errors'] and db(Portal, host = self.host).filter(Portal.id != self.id).count():
            ret['warnings']['host'] = 'host already taken by another portal'


        grouped = {}

        for inddiv, div in enumerate(self.divisions):
            if not re.match('[^\s]{3,}', div.name):
                if not 'divisions' in ret['errors']:
                    ret['errors']['divisions'] = {}
                ret['errors']['divisions'][inddiv] = 'pls enter valid name'
            if div.portal_division_type_id in grouped:
                grouped[div.portal_division_type_id] += 1
            else:
                grouped[div.portal_division_type_id] = 1

        for check_division in db(PortalDivisionType).all():
            if check_division.id not in grouped:
                grouped[check_division.id] = 0
            if check_division.min > grouped[check_division.id]:
                ret['errors']['add_division'] = 'you need at least %s `%s`' % (check_division.min, check_division.id)
                if grouped[check_division.id] == 0:
                    ret['errors']['add_division'] = 'add at least one `%s`' % (check_division.id,)
            if check_division.max < grouped[check_division.id]:
                ret['errors']['add_division'] = 'you you can have only %s `%s`' % (check_division.max, check_division.id)
        return ret

    def get_client_side_dict(self, fields='id|name, divisions.*, layout.*, logo_file_id'):
        """This method make dictionary from portal object with fields have written above"""
        return self.to_dict(fields)

    @staticmethod
    def search_for_portal_to_join(company_id, searchtext):
        """This method return all portals which are not partners current company"""
        return [port.get_client_side_dict() for port in
                db(Portal).filter(~db(CompanyPortal,
                                      company_id=company_id,
                                      portal_id=Portal.id).exists()
                                  ).filter(Portal.name.ilike("%" + searchtext + "%")).all()]


class PortalPlan(Base, PRBase):
    __tablename__ = 'portal_plan'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False,
                primary_key=True)
    name = Column(TABLE_TYPES['name'], nullable=False)

    def __init__(self, name=None):
        self.name = name


class PortalLayout(Base, PRBase):
    __tablename__ = 'portal_layout'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False,
                primary_key=True)
    name = Column(TABLE_TYPES['name'], nullable=False)
    path = Column(TABLE_TYPES['name'], nullable=False)

    def __init__(self, name=None):
        self.name = name

    def get_client_side_dict(self, fields='id|name'):
        return self.to_dict(fields)


class CompanyPortal(Base, PRBase):
    __tablename__ = 'company_portal'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
    company_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company.id'))
    portal_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('portal.id'))
    company_portal_plan_id = Column(TABLE_TYPES['id_profireader'])

    portal = relationship(Portal, backref='company_assoc')
    company = relationship(Company, backref='portal_assoc')

    def __init__(self, company_id=None, portal_id=None, portal=None, company=None,
                 company_portal_plan_id=None):
        self.company_id = company_id
        self.portal = portal
        self.company = company
        self.portal_id = portal_id
        self.company_portal_plan_id = company_portal_plan_id

    @staticmethod
    def apply_company_to_portal(company_id, portal_id):
        """Add company to CompanyPortal table. Company will be partner of this portal"""
        g.db.add(CompanyPortal(company=db(Company, id=company_id).one(),
                               portal=db(Portal, id=portal_id).one(),
                               company_portal_plan_id=db(Portal, id=portal_id).one().
                               portal_plan_id))
        g.db.flush()

    # @staticmethod
    # def show_companies_on_my_portal(company_id):
    #     """Return all companies partners at portal"""
    #     portal = Portal().own_portal(company_id).companies
    #     return portal

    @staticmethod
    def get_portals(company_id):
        """This method return all portals-partners current company"""
        return db(CompanyPortal, company_id=company_id).all()


class PortalDivision(Base, PRBase):
    __tablename__ = 'portal_division'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    cr_tm = Column(TABLE_TYPES['timestamp'])
    md_tm = Column(TABLE_TYPES['timestamp'])
    portal_division_type_id = Column(TABLE_TYPES['id_profireader'],
                                     ForeignKey('portal_division_type.id'))
    portal_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('portal.id'))
    name = Column(TABLE_TYPES['short_name'], default='')
    position = Column(TABLE_TYPES['position'])

    settings = False

    def __init__(self, portal_division_type_id=None, name=None, portal_id=None, settings=None):
        self.portal_division_type_id = portal_division_type_id
        self.name = name
        self.portal_id = portal_id
        if self.portal_division_type_id == 'company_subportal':
            self.settings = PortalDivisionSettings_company_subportal()
            self.settings.company_portal = db(CompanyPortal).filter_by(
                company_id=settings['company_id'], portal_id=portal_id).one()
            self.settings.portal_division = self
            g.db.add(self.settings)

    @orm.reconstructor
    def init_on_load(self):
        if self.portal_division_type_id == 'company_subportal':
            self.settings = db(PortalDivisionSettings_company_subportal).filter_by(
                portal_division_id=self.id).one()

    def get_client_side_dict(self, fields='id|name'):
        """This method make dictionary from portal object with fields have written above"""
        return self.to_dict(fields)

        # @staticmethod
        # def add_new_division(portal_id, name, division_type):
        #     """Add new division to current portal"""
        #     return PortalDivision(portal_id=portal_id,
        #                           name=name,
        #                           portal_division_type_id=division_type)


class PortalDivisionSettings_company_subportal(Base, PRBase):
    __tablename__ = 'portal_division_settings_company_subportal'

    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    cr_tm = Column(TABLE_TYPES['timestamp'])
    md_tm = Column(TABLE_TYPES['timestamp'])

    portal_division_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('portal_division.id'))
    company_portal_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company_portal.id'))

    company_portal = relationship(CompanyPortal)

    portal_division = relationship(PortalDivision)


class PortalDivisionType(Base, PRBase):
    __tablename__ = 'portal_division_type'
    id = Column(TABLE_TYPES['short_name'], primary_key=True)
    min = Column(TABLE_TYPES['int'])
    max = Column(TABLE_TYPES['int'])

    @staticmethod
    def get_division_types():
        """Return all divisions on profireader"""
        return db(PortalDivisionType).all()


class UserPortalReader(Base, PRBase):
    __tablename__ = 'user_portal_reader'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    user_id = Column(TABLE_TYPES['id_profireader'],
                     ForeignKey('user.id'))
    company_id = Column(TABLE_TYPES['id_profireader'],
                        ForeignKey('company.id'))
    status = Column(TABLE_TYPES['id_profireader'])
    portal_plan_id = Column(TABLE_TYPES['id_profireader'],
                            ForeignKey('portal_plan.id'))

    def __init__(self, user_id=None, company_id=None, status=None,
                 portal_plan_id=None):
        self.user_id = user_id
        self.company_id = company_id
        self.status = status
        self.portal_plan_id = portal_plan_id


