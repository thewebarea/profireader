#   don't share it with github and other public services!
#from authomatic import Authomatic
from authomatic.providers import oauth2, oauth1
from authomatic import Authomatic
#import authomatic
SECRET_KEY = '%eRg5N@%g67GN*^fn>fglD$_jh+'

CONSUMER_KEY_FB = '711484898977908'
CONSUMER_SECRET_FB = '2060f9c77949e258db43db90b54f261e'
DEV_DB_PASSWORD = 'bAnach~tArski'

OAUTH_CONFIG = {
    'facebook': {
        'class_': oauth2.Facebook,
        #'consumer_key': '711484898977908', # profireader
        #'consumer_secret': '2060f9c77949e258db43db90b54f261e', # profireader
        'consumer_key': '1457232851257658',  # cit2 # Site URL: http://cit2-lv149ui.rhcloud.com/
        'consumer_secret': '2c69f145fedbcc85c04e78d930616dab',  # cit2
        'scope': ['email'],
    },
    'google': {
        'class_': oauth2.Google,
        #'consumer_key': 'profireader',
        #'consumer_secret': '664683051441',
        'consumer_key': '664683051441-ur16e99ckrinb667sqetm9cnm09ku3c0.apps.googleusercontent.com',
        'consumer_secret': 'Ibo_eVjIXd3goANHuCSNytg1',
        'scope': ['email'],
    },
    'linkedin': {
       'class_': oauth2.LinkedIn,
       'consumer_key': '77lkpbzrk48i1z',
       'consumer_secret': 'eRchZwCprmAVVdjr',
       'scope': ['r_emailaddress'],
    },
    'microsoft': {
        'class_': oauth2.WindowsLive,
        'consumer_key': '0000000044158705',
        'consumer_secret': '69lwijkwEBWD3UifO2Mqg1C4c9hlvwPu',
        'scope': ['wl.emails'],
    },
    'twitter': {
        'class_': oauth1.Twitter,
        'consumer_key': '5kYuM1Y6BnZ59JNqKWWojBkvu',
        'consumer_secret': 'GIIbeWGq7DwOqtRPf5rKfh5xWF96ispEUVssXACFoQDNjNEbJS',
        'scope': ['email'],
    },
}

#import authomatic
#
#AUTHORIZATION = {
#
#    #===========================================================================
#    # Defaults
#    #===========================================================================
#
#    '__defaults__': { # This is an optional special item where you can define default values for all providers.
#         # You can override each default value by specifying it in concrete provider dict.
#         'sreg': ['fullname', 'country'],
#         'pape': ['http://schemas.openid.net/pape/policies/2007/06/multi-factor'],
#    },
#
#    #===========================================================================
#    # OAuth 2.0
#    #===========================================================================
#
#    'facebook': { # Provider name.
#         'class_': oauth2.Facebook,  # Provider class. Don't miss the trailing underscore!
#
#         # Provider type specific keyword arguments:
#         'short_name': 1, # Unique value used for serialization of credentials only needed by OAuth 2.0 and OAuth 1.0a.
#         'consumer_key': '711484898977908', # Key assigned to consumer by the provider.
#         'consumer_secret': '2060f9c77949e258db43db90b54f261e', # Secret assigned to consumer by the provider.
#         'scope': ['user_about_me', # List of requested permissions only needed by OAuth 2.0.
#                   'email']
#    },
#    'google': {
#         'class_': 'authomatic.providers.oauth2.Google', # Can be a fully qualified string path.
#
#         # Provider type specific keyword arguments:
#         'short_name': 2, # use authomatic.short_name() to generate this automatically
#         'consumer_key': '###################',
#         'consumer_secret': '###################',
#         'scope': ['https://www.googleapis.com/auth/userinfo.profile',
#                   'https://www.googleapis.com/auth/userinfo.email']
#    },
#    'windows_live': {
#         'class_': 'oauth2.WindowsLive', # Can be a string path relative to the authomatic.providers module.
#
#         # Provider type specific keyword arguments:
#         'short_name': 3,
#         'consumer_key': '###################',
#         'consumer_secret': '###################',
#         'scope': ['wl.basic',
#                   'wl.emails',
#                   'wl.photos']
#    },
#
#    #===========================================================================
#    # OAuth 1.0a
#    #===========================================================================
#
#    'twitter': {
#         'class_': oauth1.Twitter,
#
#         # Provider type specific keyword arguments:
#         'short_name': 4,
#         'consumer_key': '###################',
#         'consumer_secret': '###################'
#         # OAuth 1.0a doesn't need scope.
#    },
#
#    #===========================================================================
#    # OpenID
#    #===========================================================================
#
#    'oi': {
#         'class_': openid.OpenID, # OpenID only needs this.
#    },
#    'gaeoi': {
#         'class_': gaeopenid.GAEOpenID, # Google App Engine based OpenID provider.
#    },
#    'yahoo_oi': {
#         'class_': openid.Yahoo, # OpenID provider with predefined identifier 'https://me.yahoo.com'.
#         'sreg': ['email'] # This overrides the "sreg" defined in "__defaults__".
#    },
#    'google_oi': {
#         'class_': openid.Google, # OpenID provider with predefined identifier 'https://www.google.com/accounts/o8/id'.
#    }
#}
