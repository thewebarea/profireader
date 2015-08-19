from sqlalchemy import Column, ForeignKey
from db_init import Base
from db_init import db_session
from ..constants.TABLE_TYPES import TABLE_TYPES
from flask import g
from ..constants.STATUS import STATUS
from .users import User
from ..controllers.errors import StatusNonActivate
from sqlalchemy.orm import relationship
from config import Config
from utils.db_utils import db

class UserCompanyRight(Base):
    __tablename__ = 'user_company_right'
    id = Column(TABLE_TYPES['bigint'], primary_key=True)
    user_company_id = Column(TABLE_TYPES['bigint'], ForeignKey('user_company.id', onupdate='cascade'))
    company_right_id = Column(TABLE_TYPES['rights'], ForeignKey('company_right.id'))

    def __init__(self, user_company_id=None, company_right_id=None):
        self.user_company_id = user_company_id
        self.company_right_id = company_right_id

    @staticmethod
    def subscribe_to_company(company_id):

        status = STATUS()
        if not db(UserCompany, user_id=g.user_dict['id'], company_id=company_id).first():
            user_rbac = UserCompany(user_id=g.user_dict['id'], company_id=company_id,
                                    status=status.NONACTIVE())
            user_rbac.user.append(db(User, id=g.user_dict['id']).first())
            db_session.add(user_rbac)
            db_session.commit()

        else:
            raise StatusNonActivate

    @staticmethod
    def apply_request(comp_id, user_id, bool):

        status = STATUS()
        r = Right()
        if bool == 'True':
            stat = status.ACTIVE()
            r.add_rights(user_id, comp_id, Config.BASE_RIGHT_IN_COMPANY)
        else:
            stat = status.REJECT()
        db(UserCompany, company_id=comp_id, user_id=user_id,
           status=status.NONACTIVE()).update({'status': stat})
        db_session.commit()

class UserCompany(Base):

    __tablename__ = 'user_company'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    user_id = Column(TABLE_TYPES['id_profireader'])
    company_id = Column(TABLE_TYPES['id_profireader'])
    status = Column(TABLE_TYPES['id_profireader'])
    right = relationship(UserCompanyRight, backref='user_company')

    def __init__(self, user_id=None, company_id=None, status=None, right=[]):
        self.user_id = user_id
        self.company_id = company_id
        self.status = status
        self.right = right

    @staticmethod
    def check_member(company_id):

        status = STATUS()
        non_active_subscribers = []
        query = db(UserCompany, status=status.NONACTIVE(), company_id=company_id).all()
        for user in query:
            for usr in user.user:
                non_active_subscribers.append(usr)
        return non_active_subscribers

class Right(Base):
    __tablename__ = 'company_right'

    id = Column(TABLE_TYPES['rights'], primary_key=True)

    def __init__(self, id=None):
        self.id = id

    @staticmethod
    def add_rights(user_id, comp_id, rights):

        ucr = []
        for right in rights:
            ucr.append(UserCompanyRight(company_right_id=right))
        user_right = db(UserCompany, user_id=user_id, company_id=comp_id).first()
        user_right.user.append(db(User, id=user_id).first())
        user_right.right = ucr
        db_session.commit()
        return user_right

    @staticmethod
    def remove_rights(user_id, comp_id, rights):

        user_right = db(UserCompany, user_id=user_id, company_id=comp_id).first()
        for right in rights:
            user_right.right.remove(UserCompanyRight(company_right_id=right))
            db_session.commit()

    @staticmethod
    def show_rights(comp_id):

        rights = {}
        status = STATUS()
        for x in db(UserCompany, company_id=comp_id).all():
            if x.user_id not in rights:
                user = db(User, id=x.user_id).first()
                rights[x.user_id] = {'name': user.user_name(), 'rights': [], 'companies': []}
            rights[x.user_id]['rights'] = [y.company_right_id for y in db(UserCompanyRight, user_company_id=x.id).all()]
            rights[x.user_id]['companies'] = [comp.id for comp in db(UserCompany, user_id=x.user_id,
                                                                     status=status.ACTIVE()).all()]
        return rights
