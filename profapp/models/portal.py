from ..constants.TABLE_TYPES import TABLE_TYPES
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from db_init import Base, db_session
from utils.db_utils import db
from .company import Company
from .pr_base import PRBase
from ..controllers.has_right import has_right


class Portal(Base, PRBase):
    __tablename__ = 'portal'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False,
                primary_key=True)
    name = Column(TABLE_TYPES['name'])
    company_owner_id = Column(TABLE_TYPES['id_profireader'],
                              ForeignKey('company.id'))
    portal_plan_id = Column(TABLE_TYPES['id_profireader'],
                            ForeignKey('portal_plan.id'))

    divisions = relationship('PortalDivision')

    company = relationship('Company', backref='portal')

    def __init__(self, name=None,
                 portal_plan_id='55dcb92a-6708-4001-acca-b94c96260506',
                 company_owner_id=None, company=None, article=None):
        self.name = name
        self.portal_plan_id = portal_plan_id
        self.company_owner_id = company_owner_id
        self.company = company
        self.article = article

    def get_client_side_dict(self, fields='id|name, divisions.*'):
        return self.to_dict(fields)

    @staticmethod
    def own_portal(company_id):
        try:
            ret = db(Portal, company_owner_id=company_id).one()
            return ret
        except:
            pass

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


class CompanyPortal(Base, PRBase):
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
    def apply_company_to_portal(company_id, portal_id):
        db_session.add(CompanyPortal(company_id=company_id,
                                     portal_id=portal_id,
                                     company_portal_plan_id=Portal().
                                     query_portal(portal_id).
                                     portal_plan_id))
        db_session.flush()

    @staticmethod
    def show_companies_on_my_portal(company_id):
        portal = Portal().own_portal(company_id)
        return CompanyPortal().all_companies_on_portal(portal.id) if \
            portal else []

    @staticmethod
    def show_portals(company_id):
        comp_port = db(CompanyPortal, company_id=company_id).all()
        return [Portal().query_portal(portal.portal_id) for portal in
                comp_port] if comp_port else []


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

    portal = relationship(Portal)

    def __init__(self, portal_division_type_id=None,
                 name=None, portal_id=None):
        self.portal_division_type_id = portal_division_type_id
        self.name = name
        self.portal_id = portal_id


class PortalDivisionType(Base, PRBase):
    __tablename__ = 'portal_division_type'
    id = Column(TABLE_TYPES['short_name'], primary_key=True)


class UserPortalReader(Base):
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
