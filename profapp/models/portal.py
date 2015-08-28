from ..constants.TABLE_TYPES import TABLE_TYPES
from sqlalchemy import Column, ForeignKey
from db_init import Base, db_session
from utils.db_utils import db
from .company import Company
from ..controllers.has_right import has_right

class Portal(Base):

    __tablename__ = 'portal'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
    name = Column(TABLE_TYPES['name'])
    company_owner_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company.id'))
    portal_plan_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('portal_plan.id'))

    def __init__(self, name=None, portal_plan_id='55dcb92a-6708-4001-acca-b94c96260506',
                 company_owner_id=None):
        self.name = name
        self.portal_plan_id = portal_plan_id
        self.company_owner_id = company_owner_id

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

class PortalPlan(Base):

    __tablename__ = 'portal_plan'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
    name = Column(TABLE_TYPES['name'], nullable=False)

    def __init__(self, name=None):
        self.name = name

class CompanyPortal(Base):

    __tablename__ = 'company_portal'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True)
    company_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company.id'))
    portal_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('portal.id'))
    company_portal_plan_id = Column(TABLE_TYPES['id_profireader'])

    def __init__(self, company_id=None, portal_id=None, company_portal_plan_id=None):
        self.company_id = company_id
        self.portal_id = portal_id
        self.company_portal_plan_id = company_portal_plan_id

    @staticmethod
    def all_companies_on_portal(portal_id):
        comp_port = db(CompanyPortal, portal_id=portal_id).all()
        if not comp_port:
            return ['Your portal does not have any companies partners']
        comp = []
        for company in comp_port:
            comp.append(db(Company, id=company.company_id).one())
        return comp

    @staticmethod
    def apply_company_to_portal(company_id, portal_id):
        db_session.add(CompanyPortal(company_id=company_id, portal_id=portal_id,
                                     company_portal_plan_id=Portal().query_portal(portal_id).portal_plan_id))
        db_session.commit()

    @staticmethod
    def show_companies_on_my_portal(company_id):

        portal = Portal().own_portal(company_id)
        if portal:
            return CompanyPortal().all_companies_on_portal(portal.id)
        else:
            return False

    @staticmethod
    def show_my_portals(company_id):
        comp_port = db(CompanyPortal, company_id=company_id).all()
        if not comp_port:
            return ['Your company does not subscribed to any portal']
        comp = []
        for portal in comp_port:
            comp.append(Portal().query_portal(portal.portal_id))
        return comp
