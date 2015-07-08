from db_connect import metadata
from sqlalchemy import Table, Column, Integer
from sqlalchemy.orm import mapper


users_table=Table('user',metadata,
                  Column('id',Integer,primary_key=True),
                  )
class User(object):
    pass
mapper(User,users_table)