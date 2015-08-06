from sqlalchemy import Column, String, Boolean, ForeignKey
from db_init import Base


class Company(Base):
    __tablename__ = 'company'
    id = Column(String(36), primary_key=True)
    name = Column(String(60))
    portal_consist = Column(Boolean)
    user_id = Column(String(60), ForeignKey('user.id'))



    # SELECT * FROM comnapny WHERE user_has_role_in_company('user_id', comnapny.id, ['owner'])

    def __init__(self, name=None, portal_consist=False, user_id=None):
        self.name = name
        self.portal_consist = portal_consist
        self.user_id = user_id
