from sqlalchemy import Table, Column, Integer, String, Boolean
from db_init import Base

class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    portal_consist = Column(Boolean)

    def __init__(self, name, portal_consist=False):
        self.name = name
        self.portal_consist=portal_consist
