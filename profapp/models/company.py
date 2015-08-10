from sqlalchemy import Column, String, Boolean, ForeignKey, TEXT, update
from db_init import Base
from flask import g, redirect, url_for
from db_init import db_session
from .user_company_role import UserCompanyRole


class Company(Base):
    __tablename__ = 'company'
    id = Column(String(36), primary_key=True)
    name = Column(String(100), unique=True)
    portal_consist = Column(Boolean)
    user_id = Column(String(36), ForeignKey('user.id'))
    country = Column(String(100))
    region = Column(String(100))
    adress = Column(String(100))
    phone = Column(String(100))
    phone2 = Column(String(100))
    email = Column(String(100))
    short_description = Column(TEXT)

    def __init__(self, name=None, portal_consist=False, user_id=None, logo=None, country=None, region=None,
                 adress=None, phone=None, phone2=None, email=None, short_description=None):
        self.name = name
        self.portal_consist = portal_consist
        self.user_id = user_id
        self.logo = logo
        self.country = country
        self.region = region
        self.adress = adress
        self.phone = phone
        self.phone2 = phone2
        self.email = email
        self.short_description = short_description

    def query_all_companies(self, id):

        companies = db_session.query(Company).filter_by(user_id=id).all()
        query_companies = db_session.query(UserCompanyRole).filter_by(user_id=id).all()
        for x in query_companies:
            companies = companies+db_session.query(Company).filter_by(id=x.company_id).all()
        return companies

    def query_company(self, id):

        company = db_session.query(Company).filter_by(id=id).first()
        return company

    def add_comp(self, data):

        if db_session.query(Company).filter_by(name=data.get('name')).first() or data.get('name') == None:

            redirect(url_for('company.company', id=g.user.id))

        else:
            company = Company()
            for x, y in zip(data.keys(), data.values()):
                if x == 'name':
                    company.name = y
                elif x == 'short_description':
                    company.short_description = y
                elif x == 'logo':
                    company.logo = y
                elif x == 'phone':
                    company.phone = y
                elif x == 'phone2':
                    company.phone2 = y
                elif x == 'country':
                    company.country = y
                elif x == 'region':
                    company.region = y
                elif x == 'adress':
                    company.adress = y
                elif x == 'email':
                    company.email = y

            company.user_id = g.user.id
            db_session.add(company)
            db_session.commit()

    def update_comp(self, id, data):

        for x, y in zip(data.keys(), data.values()):
            db_session.query(Company).filter_by(id=id).update({x: y})
            db_session.commit()
