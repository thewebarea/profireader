from sqlalchemy import Column, ForeignKey, Integer
from db_init import Base, db_session
from ..constants.TABLE_TYPES import TABLE_TYPES
from flask import g
from ..constants.USER_ROLES import ROLES
from ..constants.STATUS import STATUS
from .users import User
from ..controllers.errors import StatusNonActivate
statuses = STATUS()


class UserCompanyRole(Base):
    __tablename__ = 'user_company_role'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'), nullable=False)
    company_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company.id'), nullable=False)
    role_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company_role.id'), nullable=False)
    status = Column(TABLE_TYPES['status'], nullable=False)

    def __init__(self, user_id=None, company_id=None, role_id=None, status=None):
        self.user_id = user_id
        self.company_id = company_id
        self.role_id = role_id
        self.status = status

    @staticmethod
    def subscribe_to_company(id):

        role = ROLES()
        if not db_session.query(UserCompanyRole).filter_by(user_id=g.user_dict['id']).filter_by(company_id=id).first():
            db_session.add(UserCompanyRole(user_id=g.user_dict['id'], company_id=id,
                                           role_id=role.ADMIN(), status=statuses.NONACTIVE()))
            db_session.commit()
        else:
            raise StatusNonActivate

    @staticmethod
    def check_member(id):

        non_active_subscribers = []
        query = db_session.query(UserCompanyRole).filter_by(status=statuses.NONACTIVE()).\
            filter_by(company_id=id).all()
        for user in query:
            non_active_subscribers.append(db_session.query(User).filter_by(id=user.user_id).first())
        return non_active_subscribers

    @staticmethod
    def apply_request(comp_id, user_id, bool):

        if bool == 'True':
            stat = statuses.ACTIVE()
        else:
            stat = statuses.REJECT()

        db_session.query(UserCompanyRole).filter_by(status=statuses.NONACTIVE()).\
            filter_by(company_id=comp_id).filter_by(user_id=user_id).update({'status': stat})
        db_session.commit()

class CompanyRole(Base):
    __tablename__ = 'company_role'
    id = Column(TABLE_TYPES['role'], primary_key=True)
