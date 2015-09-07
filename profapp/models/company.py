from sqlalchemy import Column, String, ForeignKey, update
from sqlalchemy.orm import relationship
# from db_init import Base, g.db
from ..constants.TABLE_TYPES import TABLE_TYPES
from flask import g
from config import Config
from ..constants.STATUS import STATUS
from ..constants.USER_ROLES import COMPANY_OWNER, RIGHTS
from utils.db_utils import db
from .users import User
from .files import File
from .pr_base import PRBase, Base



class Company(Base, PRBase):
    __tablename__ = 'company'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    name = Column(TABLE_TYPES['name'], unique=True)
    logo_file = Column(String(36), ForeignKey('file.id'))
    journalist_folder_file_id = Column(String(36),
                                       ForeignKey('file.id'))
    corporate_folder_file_id = Column(String(36),
                                      ForeignKey('file.id'))
    portal_consist = Column(TABLE_TYPES['boolean'])
    author_user_id = Column(TABLE_TYPES['id_profireader'],
                            ForeignKey('user.id'), nullable=False)
    country = Column(TABLE_TYPES['name'])
    region = Column(TABLE_TYPES['name'])
    address = Column(TABLE_TYPES['name'])
    phone = Column(TABLE_TYPES['phone'])
    phone2 = Column(TABLE_TYPES['phone'])
    email = Column(TABLE_TYPES['email'])
    short_description = Column(TABLE_TYPES['text'])

    def __init__(self, name=None, portal_consist=False,
                 author_user_id=None, logo_file=None,
                 country=None, region=None, address=None, phone=None,
                 phone2=None, email=None, short_description=None):
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

        # get all users in company : company.employee
        # get all users companies : user.employer

    @staticmethod
    def query_company(company_id):
        ret = db(Company, id=company_id).one()

        return ret

    @staticmethod
    def search_for_company(user_id, searchtext):

        query_companies = db(Company).filter(
            Company.name.like("%"+searchtext+"%")).all()
        ret = []
        for x in query_companies:
            ret.append(x.dict())

        return ret
        # return PRBase.searchResult(query_companies)

    def user_comp_rs(self, user):

        user.employer.append(self)
        self.employee.append(user)

    def create_company(self, passed_file=None):

        self.save()
        user_rbac = UserCompany(user_id=self.author_user_id,
                                company_id=self.id, status=STATUS.
                                ACTIVE())
        user = User.user_query(g.user_dict['id'])
        user_rbac.save()

        if passed_file:
            file = File(company_id=self.id,
                        parent_id=self.corporate_folder_file_id,
                        author=g.user_dict['name'],
                        author_user_id=g.user_dict['id'],
                        name=passed_file.filename,
                        mime=passed_file.content_type)

            db(Company, id=self.id).\
                update(
                {'logo_file': file.upload(content=passed_file.
                                          stream.read(-1)).id}
            )

        self.user_comp_rs(user)

        Right.update_rights(self.author_user_id, user_rbac.company_id,
                            COMPANY_OWNER)

    @staticmethod
    def update_comp(company_id, data, passed_file):

        comp = db(Company, id=company_id)
        upd = {x: y for x, y in zip(data.keys(), data.values())}
        comp.update(upd)

        if passed_file:
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

        g.db.commit()

    @staticmethod
    def query_employee(comp_id):

        employee = db(UserCompany, company_id=comp_id,
                      user_id=g.user_dict['id']).first()
        return employee if employee else False

    def query_owner_or_member(self, company_id):

        employee = self.query_employee(company_id)
        if not employee:
            return False
        if employee.status == STATUS().ACTIVE():
            return True

class UserCompanyRight(Base, PRBase):
    __tablename__ = 'user_company_right'
    id = Column(TABLE_TYPES['bigint'], primary_key=True)
    user_company_id = Column(TABLE_TYPES['bigint'],
                             ForeignKey('user_company.id'))
    company_right_id = Column(TABLE_TYPES['rights'],
                              ForeignKey('company_right.id'))

    def __init__(self, user_company_id=None, company_right_id=None):
        self.user_company_id = user_company_id
        self.company_right_id = company_right_id

    @staticmethod
    def apply_request(comp_id, user_id, bool):

        if bool == 'True':
            stat = STATUS().ACTIVE()
            Right().update_rights(user_id, comp_id,
                                  Config.BASE_RIGHT_IN_COMPANY)
        else:
            stat = STATUS().REJECT()
        db(UserCompany, company_id=comp_id, user_id=user_id,
           status=STATUS().NONACTIVE()).update({'status': stat})
        g.db.flush()

    @staticmethod
    def suspend_employee(comp_id, user_id):
        db(UserCompany, company_id=comp_id, user_id=user_id).\
            update({'status': STATUS.SUSPEND()})
        g.db.flush()


class UserCompany(Base, PRBase):

    __tablename__ = 'user_company'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    user_id = Column(TABLE_TYPES['id_profireader'],
                     ForeignKey('user.id'))
    company_id = Column(TABLE_TYPES['id_profireader'],
                        ForeignKey('company.id'))
    status = Column(TABLE_TYPES['id_profireader'])
    md_tm = Column(TABLE_TYPES['timestamp'])
    right = relationship(UserCompanyRight, backref='user_company')

    def __init__(self, user_id=None, company_id=None, status=None,
                 right=[]):
        self.user_id = user_id
        self.company_id = company_id
        self.status = status
        self.right = right

    @staticmethod
    def user_in_company(user_id, company_id):
        ret = db(UserCompany, user_id=user_id,
                 company_id=company_id).one()
        return ret

    def subscribe_to_company(self):

        user = User.user_query(self.user_id)
        company = Company.query_company(self.company_id)
        user.employer.append(company)
        company.employee.append(user)
        self.save()

class Right(Base):
    __tablename__ = 'company_right'

    id = Column(TABLE_TYPES['rights'], primary_key=True)

    @staticmethod
    def p(right_name):
        return {'hmm': lambda **kwargs: True}

    @staticmethod
    def update_rights(user_id, comp_id, rights):

        ucr = []
        user_right = UserCompany.user_in_company(user_id, comp_id)
        for right in rights:
            ucr.append(UserCompanyRight(company_right_id=right,
                                        user_company_id=user_right.id))
        if user_right.right:
            db(UserCompanyRight, user_company_id=user_right.id).delete()
            user_right.right = ucr
        else:
            user_right.right = ucr

    @staticmethod
    def show_rights(comp_id):

        emplo = {}
        for x in Company.query_company(comp_id).employee:
            emplo[x.id] = x.id
            user_in_company = UserCompany.user_in_company(
                user_id=x.id, company_id=comp_id)
            emplo[x.id] = {'name': x.user_name, 'user': x, 'rights': [],
                           'companies': [x.employer],
                           'status': user_in_company.status,
                           'date': user_in_company.md_tm}
            emplo[x.id]['rights'] = {y: False for y in COMPANY_OWNER}
            for r in user_in_company.right:
                emplo[x.id]['rights'][r.company_right_id] = True
        return emplo

    @staticmethod
    def suspended_employees(comp_id):

        suspended_employees = {}
        for x in Company.query_company(comp_id).employee:
            user_in_company = UserCompany.user_in_company(
                user_id=x.id,
                company_id=comp_id)
            if user_in_company.status == STATUS.SUSPEND():
                suspended_employees[x.id] = x.id
                suspended_employees[x.id] = {'name': x.user_name,
                                             'user': x,
                                             'companies': [x.employer],
                                             'date':
                                                 user_in_company.md_tm}
        return suspended_employees

    @staticmethod
    def permissions(user_id, comp_id, rights):
        ucr = []
        for right in UserCompany.user_in_company(
                user_id=user_id, company_id=comp_id).right:
            ucr.append(right.company_right_id)
        return True if set(rights) < set(ucr) else False
