from sqlalchemy import Column, String, ForeignKey, update
from db_init import Base
from ..constants.TABLE_TYPES import TABLE_TYPES
from flask import g, redirect, url_for
from db_init import db_session
from .user_company_role import UserCompanyRole
from ..constants.STATUS import STATUS
from ..constants.USER_ROLES import COMPANY_OWNER
from .users import User

def db(*args, **kwargs):
    return db_session.query(args[0]).filter_by(**kwargs)

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
    def query_all_companies(id):

        status = STATUS()
        # companies = db(Company, author_user_id=id).all()
        companies = []
        query_companies = db(UserCompanyRole, user_id=id, status=status.ACTIVE()).all()

        for x in query_companies:
            companies = companies+db(Company, id=x.company_id).all()

        return set(companies)

    @staticmethod
    def query_company(id):

        company = db(Company, id=id).first()
        return company

    @staticmethod
    def add_comp(data):

        if db(Company, name=data.get('name')).first() or data.get('name') == None:

            redirect(url_for('company.show_company'))

        else:
            comp_dict = {'author_user_id': g.user_dict['id']}
            status = STATUS()

            for x, y in zip(data.keys(), data.values()):
                comp_dict[x] = y
            company = Company(**comp_dict)
            db_session.add(company)
            db_session.commit()
            user = db(User, id=company.author_user_id).first()
            for right in COMPANY_OWNER:

                user_rbac = UserCompanyRole(user_id=company.author_user_id,
                                            company_id=company.id,
                                            status=status.ACTIVE(),
                                            right_id=right,
                                            user_rights=user)
                db_session.add(user_rbac)
                db_session.commit()

    @staticmethod
    def update_comp(id, data):

        for x, y in zip(data.keys(), data.values()):
            db(Company, id=id).update({x: y})
            db_session.commit()

    @staticmethod
    def query_subscriber_all_status(comp_id):
        return db(UserCompanyRole, company_id=comp_id, user_id=g.user_dict['id']).first()

    @staticmethod
    def query_subscriber_active_status(comp_id):

        status = STATUS()
        user = db(UserCompanyRole, company_id=comp_id, status=status.ACTIVE(), user_id=g.user_dict['id']).first()

        if not user:

            user = db(Company, id=comp_id, author_user_id=g.user_dict['id']).first()
            if user:
                return user.author_user_id
            else:
                return
        return user.user_id

    @staticmethod
    def query_owner_or_member(id):

        status = STATUS()
        if db(UserCompanyRole, status=status.ACTIVE(), company_id=id, user_id=g.user_dict['id']).first() or\
                db(Company, author_user_id=g.user_dict['id'], id=id).first():
            return True
        return False

    def query_non_active(self, id):
        ucr = UserCompanyRole()
        if self.query_owner_or_member(id):
            non_active = ucr.check_member(id)
            return non_active
        return []
