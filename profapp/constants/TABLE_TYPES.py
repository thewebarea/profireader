from sqlalchemy import Integer, String, TIMESTAMP, SMALLINT, BOOLEAN

id_type = String(50)

USER_TABLE_TYPES = {'ID': Integer,
                    'GOOGLE_ID': id_type,
                    'FACEBOOK_ID': id_type,
                    'LINKEDIN_ID': id_type,
                    'TWITTER_ID': id_type,
                    'MICROSOFT_ID': id_type,
                    'YAHOO_ID': id_type,

                    'EMAIL': String(300),
                    'FIRST_NAME':  String(300),
                    'LAST_NAME': String(300),
                    'NAME': String(601),
                    'GENDER': String(10),
                    'LINK': String(600),
                    'PHONE': String(30),

                    'ABOUT_ME': String(6000),
                    'PASSWORD': String(100),
                    'PASS_SALT': String(100),

                    'EMAIL_CONF_KEY': String(100),
                    'EMAIL_CONF_TM': TIMESTAMP,
                    'PASS_RESET_KEY': String(100),
                    'PASS_RESET_CONF_TM': TIMESTAMP,
                    'REGISTERED_VIA': SMALLINT,
                    'PROFILE_COMPLETED': BOOLEAN
                    }
