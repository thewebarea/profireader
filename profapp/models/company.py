from sqlalchemy import Column, String, ForeignKey, update
from db_init import Base
from ..constants.TABLE_TYPES import TABLE_TYPES
from flask import g, redirect, url_for
from db_init import db_session
from .user_company_role import UserCompanyRole
from ..constants.STATUS import STATUS

statuses = STATUS()
ucr = UserCompanyRole()

class Company(Base):
    __tablename__ = 'company'
    id = Column(TABLE_TYPES['id_profireader'], primary_key=True)
    name = Column(TABLE_TYPES['name'], unique=True)
    logo_file = Column(String(36), ForeignKey('file.id'))
    portal_consist = Column(TABLE_TYPES['boolean'])
    author_user_id = Column(TABLE_TYPES['id_profireader'], ForeignKey('user.id'), nullable=False)
    country = Column(TABLE_TYPES['name'])
    region = Column(TABLE_TYPES['name'])
    address = Column(TABLE_TYPES['name'])
    phone = Column(TABLE_TYPES['phone'])
    phone2 = Column(TABLE_TYPES['phone'])
    email = Column(TABLE_TYPES['email'])
    short_description = Column(TABLE_TYPES['text'])

    def __init__(self, name=None, portal_consist=False, author_user_id=None, logo_file=None, country=None, region=None,
                 address=None, phone=None, phone2=None, email=None, short_description=None):
        self.name = name
        self.portal_consist = portal_consist
        self.author_user_id = author_user_id
        self.logo_file = logo_file
        self.country = country
        self.region = region
        self.address = address
        self.phone = phone
        self.phone2 = phone2
        self.email = email
        self.short_description = short_description

    @staticmethod
    def query_all_companies(id):

        status = STATUS()
        companies = db_session.query(Company).filter_by(author_user_id=id).all()
        query_companies = db_session.query(UserCompanyRole).filter_by(user_id=id).\
            filter_by(status=status.ACTIVE()).all()
        for x in query_companies:
            companies = companies+db_session.query(Company).filter_by(id=x.company_id).all()
        return companies

    @staticmethod
    def query_company(id):

        company = db_session.query(Company).filter_by(id=id).first()
        return company

    @staticmethod
    def add_comp(data):

        if db_session.query(Company).filter_by(name=data.get('name')).first() or data.get('name') == None:

            redirect(url_for('company.show_company'))

        else:
            company = Company()
            for x, y in zip(data.keys(), data.values()):
                #Company.__table__.insert().execute({x: y})

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
                elif x == 'address':
                    company.address = y
                elif x == 'email':
                    company.email = y

            company.author_user_id = g.user_dict['id']
            db_session.add(company)
            db_session.commit()

    @staticmethod
    def update_comp(id, data):

        for x, y in zip(data.keys(), data.values()):
            db_session.query(Company).filter_by(id=id).update({x: y})
            db_session.commit()

    def query_non_active(self, id):
        if db_session.query(UserCompanyRole).filter_by(status=statuses.ACTIVE()).\
                filter_by(company_id=id).filter_by(user_id=g.user_dict['id']).first() or\
                db_session.query(Company).filter_by(author_user_id=g.user_dict['id']).\
                filter_by(id=id).first():
            non_active = ucr.check_member(id)
            return non_active
        return []
