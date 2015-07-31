from sqlalchemy import Integer, String, TIMESTAMP, SMALLINT, BOOLEAN

USER_TABLE_TYPES = {'ID': Integer,
                    'GOOGLE_ID': String(50),
                    'FACEBOOK_ID': String(50),
                    'LINKEDIN_ID': String(50),
                    'TWITTER_ID': String(50),
                    'MICROSOFT_ID': String(50),
                    'YAHOO_ID': String(50),

                    'EMAIL': String(300),
                    'FIRST_NAME':  String(300),
                    'LAST_NAME': String(300),
                    'NAME': String(601),
                    'GENDER': String(10),
                    'LINK': String(200),
                    'PHONE': String(25),

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
