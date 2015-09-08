from ..constants.TABLE_TYPES import TABLE_TYPES
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
# from db_init import Base, g.db
from flask import g
from utils.db_utils import db
from .company import Company
from .pr_base import PRBase, Base


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

    layout = relationship('PortalLayout')
    divisions = relationship('PortalDivision', backref='portal',
                             primaryjoin='Portal.id=='
                                         'PortalDivision.portal_id')
    article = relationship('ArticlePortal', backref='portal',
                           uselist=False)

    company = relationship('Company', backref='portal')
    company_portal = relationship('CompanyPortal', backref='portal')

    def __init__(self, name=None, company_portal=[],
                 portal_plan_id='55dcb92a-6708-4001-acca-b94c96260506',
                 company_owner_id=None, company=None, article=None,
                 host=None, divisions=[],
                 portal_layout_id='55e99785-bda1-4001-922f-ab974923999a'
                 ):
        self.name = name
        self.portal_plan_id = portal_plan_id
        self.company_owner_id = company_owner_id
        self.company = company
        self.article = article
        self.company_portal = company_portal
        self.host = host
        self.portal_layout_id = portal_layout_id
        self.divisions = divisions

    def create_portal(self, company_id, division_name, division_type):
        self.company = db(Company, id=company_id).one()
        self.save()
        self.divisions.append(PortalDivision.add_new_division(
            portal_id=self.id, name=division_name,
            division_type=division_type))
        self.company_portal.append(
            CompanyPortal.add_portal_to_company_portal(
                portal_plan_id=self.portal_plan_id,
                company_id=self.company_owner_id,
                portal_id=self.id))
        return self

    def get_client_side_dict(self, fields='id|name, divisions.*, '
                                          'layout.*'):
        return self.to_dict(fields)

    @staticmethod
    def own_portal(company_id):
        try:
            ret = db(Portal, company_owner_id=company_id).one()
            return ret
        except:
            return []

    @staticmethod
    def query_portal(portal_id):
        ret = db(Portal, id=portal_id).one()
        return ret

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


class CompanyPortal(Base):
    __tablename__ = 'company_portal'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False,
                primary_key=True)
    company_id = Column(TABLE_TYPES['id_profireader'],
                        ForeignKey('company.id'))
    portal_id = Column(TABLE_TYPES['id_profireader'],
                       ForeignKey('portal.id'))
    company_portal_plan_id = Column(TABLE_TYPES['id_profireader'])

    def __init__(self, company_id=None, portal_id=None,
                 company_portal_plan_id=None):
        self.company_id = company_id
        self.portal_id = portal_id
        self.company_portal_plan_id = company_portal_plan_id

    @staticmethod
    def all_companies_on_portal(portal_id):
        comp_port = db(CompanyPortal, portal_id=portal_id).all()
        return [db(Company, id=company.company_id).one() for company in
                comp_port] if comp_port else False

    @staticmethod
    def add_portal_to_company_portal(portal_plan_id,
                                     company_id,
                                     portal_id):
        return CompanyPortal(company_portal_plan_id=portal_plan_id,
                             company_id=company_id,
                             portal_id=portal_id)

    @staticmethod
    def apply_company_to_portal(company_id, portal_id):
        g.db.add(CompanyPortal(company_id=company_id,
                               portal_id=portal_id,
                               company_portal_plan_id=Portal().
                               query_portal(portal_id).
                               portal_plan_id))
        g.db.flush()

    @staticmethod
    def show_companies_on_my_portal(company_id):

        portal = Portal().own_portal(company_id)
        return CompanyPortal().all_companies_on_portal(portal.id) if \
            portal else []

    @staticmethod
    def get_portals(company_id):
        comp_port = db(CompanyPortal, company_id=company_id).all()
        return [Portal().query_portal(portal.portal_id)
                for portal in comp_port]


class PortalDivision(Base, PRBase):
    __tablename__ = 'portal_division'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    cr_tm = Column(TABLE_TYPES['timestamp'])
    md_tm = Column(TABLE_TYPES['timestamp'])
    portal_division_type_id = Column(
        TABLE_TYPES['id_profireader'],
        ForeignKey('portal_division_type.id'))
    portal_id = Column(TABLE_TYPES['id_profireader'],
                       ForeignKey('portal.id'))
    name = Column(TABLE_TYPES['short_name'], default='')

    def __init__(self, portal_division_type_id=None,
                 name=None, portal_id=None):
        self.portal_division_type_id = portal_division_type_id
        self.name = name
        self.portal_id = portal_id

    def get_client_side_dict(self, fields='id|name'):
        return self.to_dict(fields)

    @staticmethod
    def add_new_division(portal_id, name, division_type):
        return PortalDivision(portal_id=portal_id,
                              name=name,
                              portal_division_type_id=division_type)

class PortalDivisionType(Base, PRBase):

    __tablename__ = 'portal_division_type'
    id = Column(TABLE_TYPES['short_name'], primary_key=True)

    @staticmethod
    def get_division_types():
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
