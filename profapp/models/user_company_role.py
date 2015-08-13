from sqlalchemy import Column, ForeignKey, Integer
from db_init import Base
from db_init import db_session
from ..constants.TABLE_TYPES import TABLE_TYPES
from flask import g
from ..constants.USER_ROLES import ROLES, RIGHTS
from ..constants.STATUS import STATUS
from .users import User
from ..controllers.errors import StatusNonActivate
from sqlalchemy.orm import relationship, backref
statuses = STATUS()
r = RIGHTS()
def db(*args, **kwargs):
    return db_session.query(args[0]).filter_by(**kwargs)

class UserCompanyRole(Base):
    __tablename__ = 'user_company_role'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'), nullable=False)
    company_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company.id'), nullable=False)
    role_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company_role.id'), nullable=False)
    status = Column(TABLE_TYPES['status'], nullable=False)
    right_id = Column(TABLE_TYPES['role'], ForeignKey('company_right.id'))

    def __init__(self, user_id=None, company_id=None, role_id=None, status=None, right_id=None):
        self.user_id = user_id
        self.company_id = company_id
        self.role_id = role_id
        self.status = status
        self.right_id = right_id

    @staticmethod
    def subscribe_to_company(id):

        role = ROLES()
        if not db(UserCompanyRole, user_id=g.user_dict['id'], company_id=id).first():
            db_session.add(UserCompanyRole(user_id=g.user_dict['id'], company_id=id,
                                           role_id=role.ADMIN(), status=statuses.NONACTIVE()))
            db_session.commit()
        else:
            raise StatusNonActivate

    @staticmethod
    def check_member(id):

        non_active_subscribers = []
        query = db(UserCompanyRole, status=statuses.NONACTIVE(), company_id=id).all()
        for user in query:
            non_active_subscribers.append(db(User, id=user.user_id).first())
        return non_active_subscribers

    @staticmethod
    def apply_request(comp_id, user_id, bool):

        user_r = Right()
        if bool == 'True':
            stat = statuses.ACTIVE()
            user_r.query_roles(user_id, comp_id).first().right_id = user_r.insert_rights().id
            user_r.user_role.append(user_r.query_roles(user_id, comp_id).first())
            print(user_r.user_role)
        else:
            stat = statuses.REJECT()
        db(UserCompanyRole, status=statuses.NONACTIVE(), company_id=comp_id, user_id=user_id).update({'status': stat})
        db_session.commit()

class CompanyRole(Base):
    __tablename__ = 'company_role'
    id = Column(TABLE_TYPES['role'], primary_key=True)

class Right(Base):
    __tablename__ = 'company_right'

    id = Column(TABLE_TYPES['role'], primary_key=True)
    rights = Column(TABLE_TYPES['rights'])
    user_role = relationship('UserCompanyRole', backref=backref('rights_show'))

    def __init__(self, rights=None):
        self.rights = rights

    def query_roles(self, user_id, comp_id):

        query = db(UserCompanyRole, user_id=user_id, company_id=comp_id)
        return query

    @staticmethod
    def insert_rights():

        insert = Right()
        insert.rights = 'comment,manage_content,'
        db_session.add(insert)
        db_session.commit()
        return insert

    def update_rights(self, user_id, comp_id, comment=r.COMMENT(), publish='None', unpublish='None',
                      write_articles=r.WRITE_ARTICLES(), moderate_comments='None', manage_content='None',
                      manage_members='None', manage_access='None', transfer_ownership='None'):
        new_rights = db(Right, id=self.query_roles(user_id=user_id, comp_id=comp_id).first().right_id).update(
            {'rights': '{comment},{publish},{unpublish},'
                            '{write_articles},{moderate_comments},{manage_content},'
                            '{manage_members},{manage_access},'
                            '{transfer_ownership}'.format(
            comment=comment, publish=publish, unpublish=unpublish, write_articles=write_articles,
            moderate_comments=moderate_comments, manage_content=manage_content, manage_members=manage_members,
            manage_access=manage_access, transfer_ownership=transfer_ownership)})

        # insert.query_roles(user_id, comp_id).update({insert.rights: '{comment},{publish},{unpublish},{write_articles},'
        #                                                             '{moderate_comments},{manage_content},'
        #                                                             '{manage_members},{manage_access},'
        #                                                             '{transfer_ownership}'.format(
        #     comment=comment, publish=publish, unpublish=unpublish, write_articles=write_articles,
        #     moderate_comments=moderate_comments, manage_content=manage_content, manage_members=manage_members,
        #     manage_access=manage_access, transfer_ownership=transfer_ownership)})
        # insert.user_role.append(db_session.query(UserCompanyRole).filter_by(user_id=g.user_dict['id']).first())
        # print(insert.user_role)
        # print(db_session.query(UserCompanyRole).filter_by(user_id=user.id]).first().rights_show.rights)
        db_session.commit()
        return new_rights
