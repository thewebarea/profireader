from flask import request, current_app
from sqlalchemy import Column, ForeignKey
from db_init import Base, db_session
from os import urandom

from ..constants.TABLE_TYPES import USER_TABLE_TYPES

from ..constants.SOCIAL_NETWORKS import SOCIAL_NETWORKS, SOC_NET_NONE
from ..constants.USER_REGISTERED import REGISTERED_WITH_FLIPPED, \
    REGISTERED_WITH
from flask.ext.login import LoginManager, UserMixin, current_user, \
    login_user, logout_user
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from sqlalchemy import String


class User(Base, UserMixin):
    __tablename__ = 'user'
    _T = USER_TABLE_TYPES

    # PROFIREADER REGISTRATION DATA
    id = Column(_T['ID'], primary_key=True)
    profireader_email = Column(_T['EMAIL'], unique=True)
    profireader_first_name = Column(_T['FIRST_NAME'])
    profireader_last_name = Column(_T['LAST_NAME'])
    profireader_name = Column(_T['NAME'])
    profireader_gender = Column(_T['GENDER'])
    profireader_link = Column(_T['LINK'])
    profireader_phone = Column(_T['PHONE'])

    about_me = Column(_T['ABOUT_ME'])
    # SECURITY DATA

    password_hash = Column(_T['PASSWORD_HASH'])
    confirmed = Column(_T['CONFIRMED'], default=False)

    registered_on = Column(_T['REGISTERED_ON'],
                           default=datetime.datetime.utcnow)
    #status_id = Column(Integer, db.ForeignKey('status.id'))

    email_conf_key = Column(_T['EMAIL_CONF_KEY'])
    email_conf_tm = Column(_T['EMAIL_CONF_TM'])
    pass_reset_key = Column(_T['PASS_RESET_KEY'])
    pass_reset_conf_tm = Column(_T['PASS_RESET_CONF_TM'])

# FB_NET_FIELD_NAMES = ['id', 'email', 'first_name', 'last_name', 'name', 'gender', 'link', 'phone']
# SOCIAL_NETWORKS = ['PROFIREADER', 'GOOGLE', 'FACEBOOK', 'LINKEDIN', 'TWITTER', 'MICROSOFT', 'YAHOO']

    # GOOGLE
    google_id = Column(_T['GOOGLE_ID'], unique=True)
    google_email = Column(_T['EMAIL'], unique=True)
    google_first_name = Column(_T['FIRST_NAME'])
    google_last_name = Column(_T['LAST_NAME'])
    google_name = Column(_T['NAME'])
    google_gender = Column(_T['GENDER'])
    google_link = Column(_T['LINK'])
    google_phone = Column(_T['PHONE'])

    # FACEBOOK
    facebook_id = Column(_T['FACEBOOK_ID'], unique=True)
    facebook_email = Column(_T['EMAIL'], unique=True)
    facebook_first_name = Column(_T['FIRST_NAME'])
    facebook_last_name = Column(_T['LAST_NAME'])
    facebook_name = Column(_T['NAME'])
    facebook_gender = Column(_T['GENDER'])
    facebook_link = Column(_T['LINK'])
    facebook_phone = Column(_T['PHONE'])

    # LINKEDIN
    linkedin_id = Column(_T['LINKEDIN_ID'], unique=True)
    linkedin_email = Column(_T['EMAIL'], unique=True)
    linkedin_first_name = Column(_T['FIRST_NAME'])
    linkedin_last_name = Column(_T['LAST_NAME'])
    linkedin_name = Column(_T['NAME'])
    linkedin_gender = Column(_T['GENDER'])
    linkedin_link = Column(_T['LINK'])
    linkedin_phone = Column(_T['PHONE'])

    # TWITTER
    twitter_id = Column(_T['TWITTER_ID'], unique=True)
    twitter_email = Column(_T['EMAIL'], unique=True)
    twitter_first_name = Column(_T['FIRST_NAME'])
    twitter_last_name = Column(_T['LAST_NAME'])
    twitter_name = Column(_T['NAME'])
    twitter_gender = Column(_T['GENDER'])
    twitter_link = Column(_T['LINK'])
    twitter_phone = Column(_T['PHONE'])

    # MICROSOFT
    microsoft_id = Column(_T['MICROSOFT_ID'], unique=True)
    microsoft_email = Column(_T['EMAIL'], unique=True)
    microsoft_first_name = Column(_T['FIRST_NAME'])
    microsoft_last_name = Column(_T['LAST_NAME'])
    microsoft_name = Column(_T['NAME'])
    microsoft_gender = Column(_T['GENDER'])
    microsoft_link = Column(_T['LINK'])
    microsoft_phone = Column(_T['PHONE'])

    # YAHOO
    yahoo_id = Column(_T['YAHOO_ID'], unique=True)
    yahoo_email = Column(_T['EMAIL'], unique=True)
    yahoo_first_name = Column(_T['FIRST_NAME'])
    yahoo_last_name = Column(_T['LAST_NAME'])
    yahoo_name = Column(_T['NAME'])
    yahoo_gender = Column(_T['GENDER'])
    yahoo_link = Column(_T['LINK'])
    yahoo_phone = Column(_T['PHONE'])

    def __init__(self,
                 PROFIREADER_ALL=SOC_NET_NONE['PROFIREADER'],
                 GOOGLE_ALL=SOC_NET_NONE['GOOGLE'],
                 FACEBOOK_ALL=SOC_NET_NONE['FACEBOOK'],
                 LINKEDIN_ALL=SOC_NET_NONE['LINKEDIN'],
                 TWITTER_ALL=SOC_NET_NONE['TWITTER'],
                 MICROSOFT_ALL=SOC_NET_NONE['MICROSOFT'],
                 YAHOO_ALL=SOC_NET_NONE['YAHOO'],

                 about_me='',
                 #password=None,
                 confirmed=False,

                 email_conf_key=None,
                 email_conf_tm=None,
                 pass_reset_key=None,
                 pass_reset_conf_tm=None,
                 ):

        self.profireader_email = PROFIREADER_ALL['EMAIL']
        self.profireader_first_name = PROFIREADER_ALL['FIRST_NAME']
        self.profireader_last_name = PROFIREADER_ALL['LAST_NAME']
        self.profireader_name = PROFIREADER_ALL['NAME']
        self.profireader_gender = PROFIREADER_ALL['GENDER']
        self.profireader_link = PROFIREADER_ALL['LINK']
        self.profireader_phone = PROFIREADER_ALL['PHONE']

        self.about_me = about_me
        #self.password = password
        self.confirmed = confirmed

        self.registered_on = datetime.datetime.utcnow()   # here problems are possible

        self.email_conf_key = email_conf_key
        self.email_conf_tm = email_conf_tm
        self.pass_reset_key = pass_reset_key
        self.pass_reset_conf_tm = pass_reset_conf_tm

# FB_NET_FIELD_NAMES = ['id', 'email', 'first_name', 'last_name', 'name', 'gender', 'link', 'phone']

        self.google_id = GOOGLE_ALL['ID']
        self.google_email = GOOGLE_ALL['EMAIL']
        self.google_first_name = GOOGLE_ALL['FIRST_NAME']
        self.google_last_name = GOOGLE_ALL['LAST_NAME']
        self.google_name = GOOGLE_ALL['NAME']
        self.google_gender = GOOGLE_ALL['GENDER']
        self.google_link = GOOGLE_ALL['LINK']
        self.google_phone = GOOGLE_ALL['PHONE']

        self.facebook_id = FACEBOOK_ALL['ID']
        self.facebook_email = FACEBOOK_ALL['EMAIL']
        self.facebook_first_name = FACEBOOK_ALL['FIRST_NAME']
        self.facebook_last_name = FACEBOOK_ALL['LAST_NAME']
        self.facebook_name = FACEBOOK_ALL['NAME']
        self.facebook_gender = FACEBOOK_ALL['GENDER']
        self.facebook_link = FACEBOOK_ALL['LINK']
        self.facebook_phone = FACEBOOK_ALL['PHONE']

        self.linkedin_id = LINKEDIN_ALL['ID']
        self.linkedin_email = LINKEDIN_ALL['EMAIL']
        self.linkedin_first_name = LINKEDIN_ALL['FIRST_NAME']
        self.linkedin_last_name = LINKEDIN_ALL['LAST_NAME']
        self.linkedin_name = LINKEDIN_ALL['NAME']
        self.linkedin_gender = LINKEDIN_ALL['GENDER']
        self.linkedin_link = LINKEDIN_ALL['LINK']
        self.linkedin_phone = LINKEDIN_ALL['PHONE']

        self.twitter_id = TWITTER_ALL['ID']
        self.twitter_email = TWITTER_ALL['EMAIL']
        self.twitter_first_name = TWITTER_ALL['FIRST_NAME']
        self.twitter_last_name = TWITTER_ALL['LAST_NAME']
        self.twitter_name = TWITTER_ALL['NAME']
        self.twitter_gender = TWITTER_ALL['GENDER']
        self.twitter_link = TWITTER_ALL['LINK']
        self.twitter_phone = TWITTER_ALL['PHONE']

        self.microsoft_id = MICROSOFT_ALL['ID']
        self.microsoft_email = MICROSOFT_ALL['EMAIL']
        self.microsoft_first_name = MICROSOFT_ALL['FIRST_NAME']
        self.microsoft_last_name = MICROSOFT_ALL['LAST_NAME']
        self.microsoft_name = MICROSOFT_ALL['NAME']
        self.microsoft_gender = MICROSOFT_ALL['GENDER']
        self.microsoft_link = MICROSOFT_ALL['LINK']
        self.microsoft_phone = MICROSOFT_ALL['PHONE']

        self.yahoo_id = YAHOO_ALL['ID']
        self.yahoo_email = YAHOO_ALL['EMAIL']
        self.yahoo_first_name = YAHOO_ALL['FIRST_NAME']
        self.yahoo_last_name = YAHOO_ALL['LAST_NAME']
        self.yahoo_name = YAHOO_ALL['NAME']
        self.yahoo_gender = YAHOO_ALL['GENDER']
        self.yahoo_link = YAHOO_ALL['LINK']
        self.yahoo_phone = YAHOO_ALL['PHONE']

    def logged_in_via(self):
        via = None
        if self.profireader_email:
            via = REGISTERED_WITH_FLIPPED['profireader']
        else:
            short_soc_net = SOCIAL_NETWORKS[1:]
            for soc_net in short_soc_net:
                x = soc_net.lower()+'_id'
                if getattr(self, x):
                    via = REGISTERED_WITH_FLIPPED[soc_net.lower()]
                    break
        return via

    def user_name(self):
        via = self.logged_in_via()
        name = getattr(self, REGISTERED_WITH[via] + '_name')
        return name

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')


    # we use SHA256.
    # https://crackstation.net/hashing-security.htm
    # "the output of SHA256 is 256 bits (32 bytes), so the salt should be at least 32 random bytes."
    #
    # another (simplier) approach can be user here.
    # see: http://sqlalchemy-utils.readthedocs.org/en/latest/data_types.html#module-sqlalchemy_utils.types.password
    # https://pythonhosted.org/passlib/lib/passlib.context-tutorial.html#full-integration-example
    @password.setter
    def password(self, password):
        if request.endpoint == 'user.signup':
            self.password_hash = \
                generate_password_hash(password,
                                       method='pbkdf2:sha256',
                                       salt_length=32)  # salt_length=8

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db_session.add(self)
        db_session.commit()
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db_session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(profireader_email=new_email).first() \
                is not None:
            return False
        self.profireader_email = new_email
        return True


    def __repr__(self):
        return "<User(id = %r)>" % self.id
