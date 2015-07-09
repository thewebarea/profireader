from db_connect import sql_session, metadata
from sqlalchemy import Table, Column, Integer, String,Boolean
from sqlalchemy.orm import mapper

company_table=Table('company',metadata,
                    Column('id',Integer,primary_key=True),
                    Column('name',String(60)),
                    Column('portal_consist',Boolean)
                    )
class Company(object):
    query=sql_session.query_property()
    def __init__(self,name,portal_consist=False):
        self.name=name
        self.portal_consist=portal_consist
mapper(Company,company_table)

