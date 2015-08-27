from sqlalchemy import Column, String, ForeignKey, update
from sqlalchemy.orm import relationship
from db_init import Base, db_session
from ..constants.TABLE_TYPES import TABLE_TYPES
from flask import g, abort
from config import Config
from ..constants.STATUS import STATUS
from ..constants.USER_ROLES import COMPANY_OWNER, RIGHTS
from utils.db_utils import db
from .users import User
from ..controllers.errors import StatusNonActivate
from .files import File
import datetime
from ..controllers.has_right import has_right
from .pr_base import PRBase

class Company(Base, PRBase):
    __tablename__ = 'company'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    name = Column(TABLE_TYPES['name'], unique=True)
    logo_file = Column(String(36), ForeignKey('file.id'))
    journalist_folder_file_id = Column(String(36), ForeignKey('file.id'))
    corporate_folder_file_id = Column(String(36), ForeignKey('file.id'))
    portal_consist = Column(TABLE_TYPES['boolean'])
    author_user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'), nullable=False)
    country = Column(TABLE_TYPES['name'])
    region = Column(TABLE_TYPES['name'])
    address = Column(TABLE_TYPES['name'])
    phone = Column(TABLE_TYPES['phone'])
    phone2 = Column(TABLE_TYPES['phone'])
    email = Column(TABLE_TYPES['email'])
    short_description = Column(TABLE_TYPES['text'])
    user_company_rs = relationship('UserCompany', backref='company', lazy='dynamic')

    def __init__(self, name=None, portal_consist=False, author_user_id=None, logo_file=None, country=None, region=None,
                 address=None, phone=None, phone2=None, email=None, short_description=None, user_company_rs=[]):
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
        self.user_company_rs = user_company_rs

    @staticmethod
    def employee(company_id):
        ret = db(UserCompany, company_id=company_id).all()
        return ret

    @staticmethod
    def employee_rights(company_id, user_id):
        ret = db(UserCompany, company_id=company_id, user_id=user_id).one().right
        return ret

    @staticmethod
    def query_all_companies(user_id):

        companies = []
        query_companies = db(UserCompany, user_id=user_id, status=STATUS().ACTIVE()).all()
        for x in query_companies:
            companies = companies+db(Company, id=x.company_id).all()
        return set(companies)

    @staticmethod
    def search_for_company(user_id, searchtext):

        companies = []
        query_companies = db(Company).filter(Company.user_company_rs.any(user_id=user_id)).filter(Company.name.like("%"+searchtext+"%")).all()
        return PRBase.searchResult(query_companies)


    @staticmethod
    def query_company(company_id):

        company = db(Company, id=company_id).one()
        return company


    def create_company(self, data, passed_file):
        has_right(True)
        comp_dict = {'author_user_id': g.user_dict['id']}
        for x, y in zip(data.keys(), data.values()):
            comp_dict[x] = y
        company = Company(**comp_dict)
        db_session.add(company)
        db_session.flush()
        user_rbac = UserCompany(user_id=company.author_user_id,
                                company_id=company.id, status=STATUS.ACTIVE())

        file = File(company_id=company.id,
                    parent_id=company.corporate_folder_file_id,
                    author=g.user_dict['name'],
                    author_user_id=g.user_dict['id'],
                    name=passed_file.filename,
                    mime=passed_file.content_type)

        db(Company, id=company.id).\
            update(
            {'logo_file': file.upload(content=passed_file.stream.read(-1)).id}
        )

        db_session.add(user_rbac)
        db_session.flush()
        r = Right()
        r.update_rights(company.author_user_id, user_rbac.company_id, COMPANY_OWNER)

    @staticmethod
    def update_comp(company_id, data, passed_file):

        has_right(Right.permissions(g.user_dict['id'], company_id, rights=[RIGHTS.EDIT()]))
        comp = db(Company, id=company_id)
        for x, y in zip(data.keys(), data.values()):
            comp.update({x: y})

        if passed_file.filename:
            file = File(company_id=company_id,
                        parent_id=comp.one().corporate_folder_file_id,
                        author=g.user_dict['name'],
                        author_user_id=g.user_dict['id'],
                        name=passed_file.filename,
                        mime=passed_file.content_type)
            comp.update(
                {'logo_file':
                    file.upload(content=passed_file.stream.read(-1)).id}
            )

        db_session.commit()

    @staticmethod
    def query_employee(comp_id):

        employee = db(UserCompany, company_id=comp_id, user_id=g.user_dict['id']).first()
        if employee:
            return employee
        return False

    def query_owner_or_member(self, company_id):

        employee = self.query_employee(company_id)
        if not employee:
            return False
        if employee.status == STATUS().ACTIVE():
            return True

class UserCompanyRight(Base, PRBase):
    __tablename__ = 'user_company_right'
    id = Column(TABLE_TYPES['bigint'], primary_key=True)
    user_company_id = Column(TABLE_TYPES['bigint'], ForeignKey('user_company.id'))
    company_right_id = Column(TABLE_TYPES['rights'], ForeignKey('company_right.id'))

    def __init__(self, user_company_id=None, company_right_id=None):
        self.user_company_id = user_company_id
        self.company_right_id = company_right_id

    @staticmethod
    def subscribe_to_company(company_id):

        has_right(True)
        if not db(UserCompany, user_id=g.user_dict['id'], company_id=company_id).first():
            user_rbac = UserCompany(user_id=g.user_dict['id'], company_id=company_id,
                                    status=STATUS().NONACTIVE())
            user_rbac.user = db(User, id=g.user_dict['id']).one()
            db_session.add(user_rbac)
            db_session.commit()

        else:
            raise StatusNonActivate

    @staticmethod
    def apply_request(comp_id, user_id, bool):

        has_right(Right.permissions(g.user_dict['id'], comp_id, rights=[RIGHTS.ADD_EMPLOYEE()]))
        if bool == 'True':
            stat = STATUS().ACTIVE()
            Right().update_rights(user_id, comp_id, Config.BASE_RIGHT_IN_COMPANY)
        else:
            stat = STATUS().REJECT()
        db(UserCompany, company_id=comp_id, user_id=user_id,
           status=STATUS().NONACTIVE()).update({'status': stat})
        db_session.commit()

    @staticmethod
    def suspend_employee(comp_id, user_id):
        has_right(Right.permissions(g.user_dict['id'], comp_id, rights=[RIGHTS.SUSPEND_EMPLOYEE()]))
        db(UserCompany, company_id=comp_id, user_id=user_id).update({'status': STATUS.SUSPEND()})
        db_session.commit()


class UserCompany(Base, PRBase):

    __tablename__ = 'user_company'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'))
    company_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company.id'))
    status = Column(TABLE_TYPES['id_profireader'])
    md_tm = Column(TABLE_TYPES['timestamp'])
    right = relationship(UserCompanyRight, backref='user_company')

    def __init__(self, user_id=None, company_id=None, status=None, right=[],):
        self.user_id = user_id
        self.company_id = company_id
        self.status = status
        self.right = right


class Right(Base):
    __tablename__ = 'company_right'

    id = Column(TABLE_TYPES['rights'], primary_key=True)

    @staticmethod
    def update_rights(user_id, comp_id, rights):

        has_right(Right.permissions(g.user_dict['id'], comp_id, rights=[RIGHTS.MANAGE_ACCESS_COMPANY()]))
        ucr = []
        user = db(User, id=user_id).one()
        user_right = db(UserCompany, user_id=user_id, company_id=comp_id).one()
        for right in rights:
            ucr.append(UserCompanyRight(company_right_id=right, user_company_id=user_right.id))
        if user_right.right:
            db(UserCompanyRight, user_company_id=user_right.id).delete()
            user_right.right = ucr
        else:
            user_right.company = db(Company, id=comp_id).one()
            user.companies.append(user_right.company)
            user_right.user = user
            user_right.right = ucr

        db_session.commit()

    @staticmethod
    def show_rights(comp_id):

        emplo = {}
        for x in Company.employee(comp_id):
            emplo[x.user_id] = x.user_id
            emplo[x.user_id] = {'name': x.user.user_name, 'user': x.user, 'rights': [],
                                'companies': [x.user.companies], 'status': x.status,
                                'date': x.md_tm}
            emplo[x.user_id]['rights'] = {y: False for y in COMPANY_OWNER}
            for r in Company.employee_rights(comp_id, x.user_id):
                emplo[x.user_id]['rights'][r.company_right_id] = True
        return emplo

    @staticmethod
    def suspended_employees(comp_id):

        has_right(True)
        suspended_employees = {}
        for x in Company.employee(comp_id):
            if x.status == STATUS.SUSPEND():
                suspended_employees[x.user_id] = x.user_id
                suspended_employees[x.user_id] = {'name': x.user.user_name, 'user': x.user,
                                                  'companies': [x.user.companies], 'date': x.md_tm}
        return suspended_employees

    @staticmethod
    def permissions(user_id, comp_id, rights):
        ucr = []
        for right in Company.employee_rights(comp_id, user_id):
            ucr.append(right.company_right_id)
        if not set(rights) < set(ucr):
                return False
        return True
