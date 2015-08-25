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

    def __init__(self, company_id=None, portal_id=None):
        self.company_id = company_id
        self.portal_id = portal_id

    @staticmethod
    def apply_company_to_portal(company_id, portal_id):
        db_session.add(CompanyPortal(company_id=company_id, portal_id=portal_id))
        db_session.commit()

    @staticmethod
    def show_companies_on_portal(company_id):
        comp = []
        portal = db(Portal, company_owner_id=company_id).one()
        for company in db(CompanyPortal, portal_id=portal.id).all():
            comp.append(db(Company, id=company.company_id).one())
        return comp
