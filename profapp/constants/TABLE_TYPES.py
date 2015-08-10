from sqlalchemy import Integer, String, TIMESTAMP, SMALLINT, BOOLEAN
from sqlalchemy_utils.types.phone_number import PhoneNumberType
from sqlalchemy_utils import URLType

id_soc_net_type = String(50)
# read this about UUID:
# http://stackoverflow.com/questions/183042/how-can-i-use-uuids-in-sqlalchemy
# http://stackoverflow.com/questions/20532531/how-to-set-a-column-default-to-a-postgresql-function-using-sqlalchemy
id_profireader_type = Integer
phone_type = PhoneNumberType(country_code='UA')  #(country_code='UA')
#http://sqlalchemy-utils.readthedocs.org/en/latest/data_types.html#module-sqlalchemy_utils.types.url
# read also https://github.com/gruns/furl
link_type = URLType  # user = User(website=u'www.example.com')
email_type = String(300)

USER_TABLE_TYPES = {'ID': id_profireader_type,
                    'GOOGLE_ID': id_soc_net_type,
                    'FACEBOOK_ID': id_soc_net_type,
                    'LINKEDIN_ID': id_soc_net_type,
                    'TWITTER_ID': id_soc_net_type,
                    'MICROSOFT_ID': id_soc_net_type,
                    'YAHOO_ID': id_soc_net_type,

                    'EMAIL': email_type,
                    'FIRST_NAME':  String(300),
                    'LAST_NAME': String(300),
                    'NAME': String(601),
                    'GENDER': String(10),
                    'LINK': link_type,
                    'PHONE': phone_type,

                    'ABOUT_ME': String(6000),
                    'PASSWORD_HASH': String(128),  # String(128) SHA-256

                    'REGISTERED_ON': TIMESTAMP,

                    'EMAIL_CONF_KEY': String(100),
                    'EMAIL_CONF_TM': TIMESTAMP,
                    'PASS_RESET_KEY': String(100),
                    'PASS_RESET_CONF_TM': TIMESTAMP,
                    'PROFILE_COMPLETED': BOOLEAN
                    }
