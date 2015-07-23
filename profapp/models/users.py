from sqlalchemy import Table, Column, Integer
from sqlalchemy.orm import mapper
from db_connect import sql_session, metadata

users_table = Table('user', metadata, Column('id', Integer, primary_key=True))
class User(object):
    query = sql_session.query_property()

mapper(User, users_table)
