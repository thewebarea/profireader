from sqlalchemy import Column, String, ForeignKey
from db_init import Base
from ..constants.TABLE_TYPES import USER_TABLE_TYPES

class UserCompanyRole(Base):
    __tablename__ = 'user_company_role'
    id = Column(String(36), primary_key=True)
    user_id = Column(USER_TABLE_TYPES['ID'], ForeignKey('user.id'))
    company_id = Column(String(36), ForeignKey('company.id'))
    role_id = Column(String(36), ForeignKey('company_role.id'))

    def __init__(self, user_id=None, company_id=None, role_id=None):
        self.user_id = user_id
        self.company_id = company_id
        self.role_id = role_id

class CompanyRole(Base):
    __tablename__ = 'company_role'
    id = Column(String(36), primary_key=True)
    name = Column(String(50))

    def __init__(self, name=None):
        self.name = name
