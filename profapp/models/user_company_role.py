from sqlalchemy import Column, String, ForeignKey, Integer
from db_init import Base
from ..constants.TABLE_TYPES import TABLE_TYPES

class UserCompanyRole(Base):
    __tablename__ = 'user_company_role'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'), nullable=False)
    company_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company.id'), nullable=False)
    role_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('company_role.id'), nullable=False)

    def __init__(self, user_id=None, company_id=None, role_id=None):
        self.user_id = user_id
        self.company_id = company_id
        self.role_id = role_id

class CompanyRole(Base):
    __tablename__ = 'company_role'
    id = Column(TABLE_TYPES['role'], primary_key=True)

    def __init__(self, name=None):
        self.name = name
