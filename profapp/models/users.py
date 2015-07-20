from sqlalchemy import Column, Integer, String, TIMESTAMP, SMALLINT
#from db_connect import sql_session, metadata
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(300))
    first_name = Column(String(300))
    second_name = Column(String(300))
    password = Column(String(100))
    pass_salt = Column(String(100))
    fb_uid = Column(Integer)
    google_uid = Column(Integer)
    twitter_uid = Column(Integer)
    linkedin_uid = Column(Integer)
    email_conf_key = Column(String(100))
    email_conf_tm = Column(TIMESTAMP)
    pass_reset_key = Column(String(100))
    pass_reset_conf_tm = Column(TIMESTAMP)
    registered_via = Column(SMALLINT)

    def __init__(self, email='guest@profireader.com', first_name=None,
                 second_name=None, password=None, pass_salt=None, fb_uid=None,
                 google_uid=None, twitter_uid=None, linkedin_uid=None,
                 email_conf_key=None, email_conf_tm=None, pass_reset_key=None,
                 pass_reset_conf_tm=None, registered_via=None,):
        self.email = email
        self.first_name = first_name
        self.second_name = second_name
        self.password = password
        self.pass_salt = pass_salt
        self.fb_uid = fb_uid
        self.google_uid = google_uid
        self.twitter_uid = twitter_uid
        self.linkedin_uid = linkedin_uid
        self.email_conf_key = email_conf_key
        self.email_conf_tm = email_conf_tm
        self.pass_reset_key = pass_reset_key
        self.pass_reset_conf_tm = pass_reset_conf_tm
        self.registered_via = registered_via

    def __repr__(self):
        return "<User(e_mail = '%s', id = '%d', name='%s', fullname='%s')>" % (
            self.email, self.id, self.fullname, self.password)
