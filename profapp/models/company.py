from sqlalchemy import Column, String, ForeignKey, UniqueConstraint  # , update
from sqlalchemy.orm import relationship, backref
# from db_init import Base, db_session
from sqlalchemy import Column, String, ForeignKey, update
from sqlalchemy.orm import relationship
# from db_init import Base, g.db
from ..constants.TABLE_TYPES import TABLE_TYPES
from flask import g
from config import Config
from ..constants.STATUS import STATUS
from ..constants.USER_ROLES import COMPANY_OWNER_RIGHTS, RIGHTS
from utils.db_utils import db
from .users import User
from .files import File, FileContent
from .pr_base import PRBase
from sqlalchemy import CheckConstraint
from flask import abort
# from db_init import db_session
# from functools import reduce
from .rights import Right, ALL_AVAILABLE_RIGHTS_FALSE
from ..controllers.request_wrapers import check_rights
from flask.ext.login import current_user
from .files import File
from .pr_base import PRBase, Base
from ..controllers import errors


class Company(Base, PRBase):
    __tablename__ = 'company'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    name = Column(TABLE_TYPES['name'], unique=True)
    logo_file = Column(String(36), ForeignKey('file.id'))
    journalist_folder_file_id = Column(String(36),
                                       ForeignKey('file.id'))
    corporate_folder_file_id = Column(String(36),
                                      ForeignKey('file.id'))
#    portal_consist = Column(TABLE_TYPES['boolean'])
    author_user_id = Column(TABLE_TYPES['id_profireader'],
                            ForeignKey('user.id'),
                            nullable=False)
    country = Column(TABLE_TYPES['name'])
    region = Column(TABLE_TYPES['name'])
    address = Column(TABLE_TYPES['name'])
    phone = Column(TABLE_TYPES['phone'])
    phone2 = Column(TABLE_TYPES['phone'])
    email = Column(TABLE_TYPES['email'])
    short_description = Column(TABLE_TYPES['text'])
    portal = relationship('Portal', secondary='company_portal')
    own_portal = relationship('Portal', backref='own_company',
                              foreign_keys='Portal.company_owner_id',
                              uselist=False)

    # todo: add company time creation

    owner = relationship('User', backref='companies')
    employees = relationship('User', secondary='user_company',
                             lazy='dynamic')
    logo_file_relationship = relationship('File',
                                          uselist=False,
                                          backref='logo_owner_company',
                                          foreign_keys='Company.'
                                                       'logo_file')
    # get all users in company : company.employees
    # get all users companies : user.employers

    def create_new_company(self, user_id):

    #TODO VK TO VK: CHECK G>USER INSTANSE QUERY
        user = g.db.query(User).get(user_id)
        user_company = UserCompany(status=STATUS.ACTIVE(),
                                   rights=COMPANY_OWNER_RIGHTS)
        user_company.employer = self
        user.employer_assoc.append(user_company)  # .all() added
        user.companies.append(self)

        return self

    def suspended_employees(self):
        suspended_employees = [x.to_dict('md_tm, employee.*,'
                                         'employee.employers.*')
                               for x in self.employee_assoc
                               if x.status == STATUS.SUSPEND()]
        return suspended_employees

    @staticmethod
    def query_company(company_id):
        ret = db(Company, id=company_id).one()
        return ret

    @staticmethod
    def search_for_company(user_id, searchtext):
        query_companies = db(Company).filter(
            Company.name.like("%" + searchtext + "%")).filter.all()
        ret = []
        for x in query_companies:
            ret.append(x.dict())

        return ret
        # return PRBase.searchResult(query_companies)

    @staticmethod
    def update_comp(company_id, data, passed_file):

        company = db(Company, id=company_id)
        upd = {x: y for x, y in zip(data.keys(), data.values())}
        company.update(upd)

        if passed_file:
            file = File(company_id=company_id,
                        parent_id=company.one().corporate_folder_file_id,
                        author_user_id=g.user_dict['id'],
                        name=passed_file.filename,
                        mime=passed_file.content_type)
            company.update(
                {'logo_file': file.upload(
                    content=passed_file.stream.read(-1)).id}
            )
        # db_session.flush()

    @staticmethod
    def query_employee(company_id):

        employee = db(UserCompany, company_id=company_id,
                      user_id=g.user_dict['id']).first()
        return employee if employee else False

    def query_owner_or_member(self, company_id):

        employee = self.query_employee(company_id)
        if not employee:
            return False
        if employee.status == STATUS().ACTIVE():
            return True

    @staticmethod
    def search_for_company_to_join(user_id, searchtext):
        return [company.get_client_side_dict() for company in
                db(Company).filter(~db(UserCompany, user_id=user_id,
                                       company_id=Company.id).exists()).
                filter(Company.name.ilike("%" + searchtext + "%")
                       ).all()]

    def get_client_side_dict(self, fields='id|name'):
        return self.to_dict(fields)


def simple_permissions(rights):  # .p(right_name)
    set_of_rights = frozenset(rights)

    def business_rule(**kwargs):
        if 'company_id' in kwargs.keys():
            company_object = kwargs['company_id']
        elif 'company' in kwargs.keys():
            company_object = kwargs['company']
        else:
            company_object = None
        if 'user_id' in kwargs.keys():
            user_object = kwargs['user_id']
        elif 'user' in kwargs.keys():
            user_object = kwargs['user']
        else:
            user_object = None

        def user_company_permissions_rule(rights):
            return UserCompany.permissions(rights, user_object,
                                           company_object)

        return user_company_permissions_rule

    return {set_of_rights: business_rule}


class UserCompany(Base, PRBase):
    __tablename__ = 'user_company'

    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    user_id = Column(TABLE_TYPES['id_profireader'],
                     ForeignKey('user.id'),
                     nullable=False)
    company_id = Column(TABLE_TYPES['id_profireader'],
                        ForeignKey('company.id'),
                        nullable=False)
    status = Column(TABLE_TYPES['id_profireader'])
    md_tm = Column(TABLE_TYPES['timestamp'])
    rights = Column(TABLE_TYPES['bigint'],
                    CheckConstraint('rights >= 0',
                                    name='unsigned_rights'))

    employer = relationship('Company', backref='employee_assoc')
    employee = relationship('User',
                            backref=backref('employer_assoc',
                                            lazy='dynamic'))
    UniqueConstraint('user_id', 'company_id', name='user_id_company_id')

    # todo: check handling md_tm

    def __init__(self, user_id=None, company_id=None, status=None,
                 rights=0):
        self.user_id = user_id
        self.company_id = company_id
        self.status = status
        self.rights = rights

    @staticmethod
    def user_in_company(user_id, company_id):
        ret = db(
            UserCompany, user_id=user_id, company_id=company_id).one()
        return ret

    # do we provide any rights to user at subscribing?
    def subscribe_to_company(self):
        if db(UserCompany, user_id=self.user_id,
              company_id=self.company_id).count():
            raise errors.AlreadyJoined({'message': 'UserAlreadyJoined'})
        self.employee = User.user_query(self.user_id)
        self.employer = db(Company, id=self.company_id).one()
        self.save()

    @staticmethod
    def suspend_employee(company_id, user_id):
        db(UserCompany, company_id=company_id, user_id=user_id). \
            update({'status': STATUS.SUSPEND()})
        # db_session.flush()

    @staticmethod
    def apply_request(company_id, user_id, bool):
        if bool == 'True':
            stat = STATUS().ACTIVE()
            UserCompany.update_rights(user_id,
                                      company_id,
                                      Config.BASE_RIGHT_IN_COMPANY)
        else:
            stat = STATUS().REJECT()
        db(UserCompany, company_id=company_id, user_id=user_id,
           status=STATUS().NONACTIVE()).update({'status': stat})

    ## corrected
    @staticmethod
    @check_rights(simple_permissions([]))
    def update_rights(user_id, company_id, new_rights):
        new_rights_binary = Right.transform_rights_into_integer(new_rights)
        user_company = db(UserCompany, user_id=user_id,
                          company_id=company_id)
        rights_dict = {'rights': new_rights_binary}
        user_company.update(rights_dict)

    #  corrected
    @staticmethod
    def show_rights(company_id):
        emplo = {}
        for user in db(Company, id=company_id).one().employees:
            user_company = user.employer_assoc. \
                filter_by(company_id=company_id).first()
            emplo[user.id] = {'id': user.id,
                              'name': user.user_name,
                              # TODO (AA): don't pass user object
                              'user': user,
                              'rights': {},
                              'companies': [user.employers],
                              'status': user_company.status,
                              'date': user_company.md_tm}

            emplo[user.id]['rights'] = \
                Right.transform_rights_into_set(user_company.rights)
            # earlier it was a dictionary:
            # {'right_1': True, 'right_2': False, ...}
        return emplo

    @staticmethod
    def permissions(needed_rights_iterable, user_object, company_object):
        if not (user_object and company_object):
            return True
        user = user_object
        company = company_object
        if type(user_object) is str:
            user = g.db.query(User).filter_by(id=user_object).first()
        if type(company_object) is str:
            company = g.db.query(Company).\
                filter_by(id=company_object).first()

        needed_rights_int = \
            Right.transform_rights_into_integer(needed_rights_iterable)

        # available_rights = \
        #     [user_company.rights for user_company in user.employers
        #      if user_company.company == company
        #      ][0] or 0

        user_company = \
            user.employer_assoc.filter_by(company_id=company.id).first()

        available_rights = user_company.rights if user_company else 0

        if (available_rights & needed_rights_int) != needed_rights_int:
            return abort(403)
        else:
            return True
