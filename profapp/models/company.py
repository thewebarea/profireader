from sqlalchemy import Column, String, ForeignKey, update
from db_init import Base
from ..constants.TABLE_TYPES import TABLE_TYPES
from flask import g
from db_init import db_session
from .user_company_role import UserCompany, Right
from ..constants.STATUS import STATUS
from ..constants.USER_ROLES import COMPANY_OWNER
from utils.db_utils import db

class Company(Base):
    __tablename__ = 'company'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    name = Column(TABLE_TYPES['name'], unique=True)
    logo_file = Column(String(36), ForeignKey('file.id'))
    portal_consist = Column(TABLE_TYPES['boolean'])
    author_user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'), nullable=False)
    country = Column(TABLE_TYPES['name'])
    region = Column(TABLE_TYPES['name'])
    address = Column(TABLE_TYPES['name'])
    phone = Column(TABLE_TYPES['phone'])
    phone2 = Column(TABLE_TYPES['phone'])
    email = Column(TABLE_TYPES['email'])
    short_description = Column(TABLE_TYPES['text'])

    def __init__(self, name=None, portal_consist=False, author_user_id=None, logo_file=None, country=None, region=None,
                 address=None, phone=None, phone2=None, email=None, short_description=None):
        self.name = name
        self.portal_consist = portal_consist
        self.author_user_id = author_user_id
        self.logo_file = logo_file
        self.country = country
        self.region = region
        self.address = address
        self.phone = phone
        self.phone2 = phone2
        self.email = email
        self.short_description = short_description

    @staticmethod
    def query_all_companies(user_id):

        status = STATUS()
        companies = []
        query_companies = db(UserCompany, user_id=user_id, status=status.ACTIVE()).all()
        for x in query_companies:
            companies = companies+db(Company, id=x.company_id).all()
        return set(companies)

    @staticmethod
    def query_company(company_id):

        company = db(Company, id=company_id).first()
        return company

    @staticmethod
    # create_company
    def create_company(data):

        comp_dict = {'author_user_id': g.user_dict['id']}
        status = STATUS()
        for x, y in zip(data.keys(), data.values()):
            comp_dict[x] = y
        company = Company(**comp_dict)
        db_session.add(company)
        db_session.commit()
        user_rbac = UserCompany(user_id=company.author_user_id,
                                company_id=company.id,
                                status=status.ACTIVE())
        db_session.add(user_rbac)
        db_session.commit()
        r = Right()
        r.add_rights(company.author_user_id, company.id, COMPANY_OWNER)

    @staticmethod
    def update_comp(company_id, data):

        for x, y in zip(data.keys(), data.values()):
            db(Company, id=company_id).update({x: y})
            db_session.commit()

    @staticmethod
    def query_employee(comp_id):

        employee = db(UserCompany, company_id=comp_id, user_id=g.user_dict['id']).first()
        if employee:
            return employee
        return False

    def query_owner_or_member(self, company_id):

        status = STATUS()
        employee = self.query_employee(company_id)
        if not employee:
            return False
        if employee.status == status.ACTIVE():
            return True

    def query_non_active(self, company_id):
        ucr = UserCompany()
        if self.query_owner_or_member(company_id):
            non_active = ucr.check_member(company_id)
            return non_active
        return []
