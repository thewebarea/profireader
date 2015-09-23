from sqlalchemy import Column, String, ForeignKey, UniqueConstraint, Enum  # , update
from sqlalchemy.orm import relationship, backref
# from db_init import Base, db_session
from flask.ext.login import current_user
from sqlalchemy import Column, String, ForeignKey, update
from sqlalchemy.orm import relationship
from ..constants.TABLE_TYPES import TABLE_TYPES
from flask import g
from config import Config
from ..constants.STATUS import STATUS
from ..constants.USER_ROLES import COMPANY_OWNER_RIGHTS
from utils.db_utils import db
from .users import User
from sqlalchemy import CheckConstraint
from flask import abort
from .rights import Right
from ..controllers.request_wrapers import check_rights
from .files import File
from .pr_base import PRBase, Base
from ..controllers import errors
from ..constants.STATUS import STATUS_NAME
from ..models.rights import get_my_attributes


class Company(Base, PRBase):
    __tablename__ = 'company'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    name = Column(TABLE_TYPES['name'], unique=True)
    logo_file = Column(TABLE_TYPES['id_profireader'], ForeignKey('file.id'))
    journalist_folder_file_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('file.id'))
    corporate_folder_file_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('file.id'))
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
    portal = relationship('Portal', secondary='company_portal', backref=backref('companies',
                                                                                lazy='dynamic'))
    own_portal = relationship('Portal',
                              backref="own_company", uselist=False,
                              foreign_keys='Portal.company_owner_id',
                              )
    user_owner = relationship('User', backref='companies')
    # employees = relationship('User', secondary='user_company',
    #                          lazy='dynamic')
    # todo: add company time creation
    logo_file_relationship = relationship('File',
                                          uselist=False,
                                          backref='logo_owner_company',
                                          foreign_keys='Company.logo_file')
    # get all users in company : company.employees
    # get all users companies : user.employers

    def create_new_company(self):
        """Add new company to company table and make all necessary relationships,
        if company with this name already exist raise DublicateName"""
        if db(Company, name=self.name).count():
            raise errors.DublicateName({
                'message': 'Company name %(name)s already exist. Please choose another name',
                'data': self.get_client_side_dict()})
        user_company = UserCompany(status=STATUS.ACTIVE(),
                                   rights=COMPANY_OWNER_RIGHTS)
        user_company.employer = self
        g.user.employer_assoc.append(user_company)
        g.user.companies.append(self)
        return self

    def suspended_employees(self):
        """Show all suspended employees from company. Before define method you should have
        query with one company"""
        suspended_employees = [x.to_dict('md_tm, employee.*,'
                                         'employee.employers.*')
                               for x in self.employee_assoc
                               if x.status == STATUS.SUSPENDED()]
        return suspended_employees

    @staticmethod
    def query_company(company_id):
        """Method return one company"""
        ret = db(Company, id=company_id).one()
        return ret

    @staticmethod
    def search_for_company(user_id, searchtext):
        """Return all companies which are not current user employers yet"""
        query_companies = db(Company).filter(
            Company.name.like("%" + searchtext + "%")).filter.all()
        ret = []
        for x in query_companies:
            ret.append(x.dict())

        return ret
        # return PRBase.searchResult(query_companies)

    @staticmethod
    def update_comp(company_id, data, passed_file):
        """Edit company. Pass to data parameters which will be edited"""
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
    def search_for_company_to_join(user_id, searchtext):
        """Return all companies which are not current user employers yet"""
        return [company.get_client_side_dict() for company in
                db(Company).filter(~db(UserCompany, user_id=user_id,
                                       company_id=Company.id).exists()).
                filter(Company.name.ilike("%" + searchtext + "%")
                       ).all()]

    def get_client_side_dict(self, fields='id|name'):
        """This method make dictionary from portal object with fields have written above"""
        return self.to_dict(fields)


def forbidden_for_current_user(rights, **kwargs):
    if 'user_id' in kwargs.keys():
        user_id = kwargs['user_id']
    elif 'user' in kwargs.keys():
        user_id = kwargs['user'].id
    else:
        user_id = None

    rez = current_user.id != user_id
    return rez


def simple_permissions(rights):
    set_of_rights = frozenset(rights)

    def business_rule(rights, **kwargs):
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
            user_object = current_user

        return UserCompany.permissions(rights, user_object, company_object)

    return {set_of_rights: business_rule}


class UserCompany(Base, PRBase):
    __tablename__ = 'user_company'

    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'), nullable=False)
    company_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company.id'), nullable=False)

    # TODO (AA to AA): create a correspondent column with the enum type in DB
    status = Column(Enum(*tuple(map(lambda l: getattr(l, 'lower')(),
                                get_my_attributes(STATUS_NAME))),
                         name='status_name_type'), nullable=False)

    md_tm = Column(TABLE_TYPES['timestamp'])

    confirmed = Column(TABLE_TYPES['boolean'], default=False, nullable=False)
    _banned = Column(TABLE_TYPES['boolean'], default=False, nullable=False)

    rights = Column(TABLE_TYPES['bigint'], CheckConstraint('rights >= 0', name='unsigned_rights'))

    employer = relationship('Company', backref='employee_assoc')
    employee = relationship('User', backref=backref('employer_assoc', lazy='dynamic'))
    UniqueConstraint('user_id', 'company_id', name='user_id_company_id')

    # todo (AA to AA): check handling md_tm

    def __init__(self, user_id=None, company_id=None, status=None,
                 rights=0):
        self.user_id = user_id
        self.company_id = company_id
        self.status = status
        self.rights = rights

    # @staticmethod
    # def user_in_company(user_id, company_id):
    #     """Return user (status, rights) in some company"""
    #     ret = db(UserCompany, user_id=user_id, company_id=company_id).one()
    #     return ret

    # do we provide any rights to user at subscribing? Not yet
    def subscribe_to_company(self):
        """Add user to company with non-active status. After that Employer can accept request,
        and add necessary rights, or reject this user. Method need instance of class with
        parameters : user_id, company_id, status"""
        if db(UserCompany, user_id=self.user_id,
              company_id=self.company_id).count():
            raise errors.AlreadyJoined({
                'message': 'user already joined to company %(name)s',
                'data': self.get_client_side_dict()})
        self.employee = User.user_query(self.user_id)
        self.employer = db(Company, id=self.company_id).one()
        self.save()

    @staticmethod
    def suspend_employee(company_id, user_id):
        """This method make status employee in this company suspended"""
        db(UserCompany, company_id=company_id, user_id=user_id). \
            update({'status': STATUS.SUSPENDED()})
        # db_session.flush()

    @staticmethod
    def apply_request(company_id, user_id, bool):
        """Method which define when employer apply or reject request from some user to
        subscribe to this company. If bool == True(Apply) - update rights to basic rights in company
        and status to active, If bool == False(Reject) - just update status to rejected."""
        if bool == 'True':
            stat = STATUS.ACTIVE()
            UserCompany.update_rights(user_id,
                                      company_id,
                                      Config.BASE_RIGHT_IN_COMPANY)
        else:
            stat = STATUS.REJECTED()
        db(UserCompany, company_id=company_id, user_id=user_id,
           status=STATUS.NONACTIVE()).update({'status': stat})

    @staticmethod
    @check_rights(simple_permissions([Right['manage_access_company']]))
    @check_rights({frozenset(): forbidden_for_current_user})
    def update_rights(user_id, company_id, new_rights):
        """This method defines for update user-rights in company. Apply list of rights"""
        new_rights_binary = Right.transform_rights_into_integer(new_rights)
        user_company = db(UserCompany, user_id=user_id, company_id=company_id)
        rights_dict = {'rights': new_rights_binary}
        user_company.update(rights_dict)

    #  corrected
    @staticmethod
    def show_rights(company_id):
        """Show all rights all users in current company with all statuses"""
        emplo = {}
        for user in db(Company, id=company_id).one().employees:
            user_company = user.employer_assoc. \
                filter_by(company_id=company_id).one()
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
    def search_for_user_to_join(company_id, searchtext):
        """Return all users in current company which have characters
        in their name like searchtext"""
        return [user.to_dict('profireader_name|id') for user in
                db(User).filter(~db(UserCompany, user_id=User.id, company_id=company_id).exists()).
                filter(User.profireader_name.ilike("%" + searchtext + "%")).all()]

    @staticmethod
    def permissions(needed_rights_iterable, user_object, company_object):

        needed_rights_int = Right.transform_rights_into_integer(needed_rights_iterable)

        if not (user_object and company_object):
            available_rights = 0  # earlier it returned True (exception should be raised here?)
        else:
            user = user_object
            company = company_object
            if type(user_object) is str:
                user = g.db.query(User).filter_by(id=user_object).first()
                if not user:
                    return abort(400)
            if type(company_object) is str:
                company = g.db.query(Company).filter_by(id=company_object).first()
                if not company:
                    return abort(400)

            user_company = user.employer_assoc.filter_by(company_id=company.id).first()

            available_rights = user_company.rights if user_company else 0

        if (available_rights & needed_rights_int) != needed_rights_int:
            return abort(403)
        else:
            return True


class CompanyRoleRights(Base, PRBase):
    __tablename__ = 'company_role_rights'

    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    company_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company.id'))
    role = Column(TABLE_TYPES['string_30'])

    _rights_def = \
        Column(TABLE_TYPES['bigint'],
               CheckConstraint('rights >= 0', name='unsigned_profireader_rights_def'),
               default=0, nullable=False)

    _rights_undef = \
        Column(TABLE_TYPES['bigint'],
               CheckConstraint('rights >= 0', name='unsigned_profireader_rights_undef'),
               default=0, nullable=False)  # or default=COMPANY_OWNER_RIGHTS?

    CheckConstraint('_rights_def & _rights_undef = 0', name='ck_company_role_rights')

    # employers = relationship('Company', secondary='user_company',
    #                          backref=backref("employees", lazy='dynamic'))  # Correct

    @property
    def rights_int(self):
        return self._rights_def, self._rights_undef

    @rights_int.setter
    def rights_int(self, rights_def_undef_int=(0, 0)):
        # Some explanation is needed.
        # if rights_defined is 1 on some bit then this right (permission) is available.
        # if 0 then we should check the value of rights_undefined column
        # if it is really 0 then right (permission) is not available.
        # if it is 1 then this right (permission) should be taken from user_company table.
        # such construction of rights defines the CheckConstraint presented below.
        if rights_def_undef_int[0] & rights_def_undef_int[1]:
            raise Exception

        self._rights_def = rights_def_undef_int[0]
        self._rights_undef = rights_def_undef_int[1]

    @property
    def rights_set(self):
        return tuple(map(Right.transform_rights_into_set, self.rights_int))

    @rights_set.setter
    #  rights_def_undef_iterable may be a tuple of sets or lists
    def rights_set(self, rights_def_undef_iterable=([], [])):
        # Some explanation is needed.
        # if rights_defined is 1 on some bit then this right (permission) is available.
        # if 0 then we should check the value of rights_undefined column
        # if it is really 0 then right (permission) is not available.
        # if it is 1 then this right (permission) should be taken from user_company table.
        # such construction of rights defines the CheckConstraint presented below.
        if set(rights_def_undef_iterable[0]) & set(rights_def_undef_iterable[1]):
            raise Exception
        rights_def_undef_int = tuple(
            map(Right.transform_rights_into_integer, rights_def_undef_iterable)
        )

        (self._rights_def, self._rights_undef) = rights_def_undef_int

    @property
    def rights_defined_int(self):
        return self.rights_int[0]

    @rights_defined_int.setter
    def rights_defined_int(self, rights_def_int):
        self.rights_int = (rights_def_int, self.rights_int[1])

    @property
    def rights_undefined_int(self):
        return self.rights_int[1]

    @rights_undefined_int.setter
    def rights_undefined_int(self, rights_undef_int):
        self.rights_int = (self.rights_int[0], rights_undef_int)

    @property
    def rights_defined_set(self):
        return self.rights_set[0]

    @rights_defined_set.setter
    def rights_defined_set(self, rights_def_set):
        self.rights_set = (rights_def_set, self.rights_set[1])

    @property
    def rights_undefined_set(self):
        return self.rights_set[1]

    @rights_undefined_set.setter
    def rights_undefined_set(self, rights_undef_set):
        self.rights_set = (self.rights_set[0], rights_undef_set)

    def __init__(self, rights_set=([], [])):
        super(CompanyRoleRights, self).__init__()
        self.rights_set = rights_set

