import os

def database_uri(host, username, password, db_name):
    return 'postgresql+psycopg2://{username}:{password}@{host}/{db_name}'. \
        format(**{'db_name': db_name,
                  'host': host,
                  'username': username,
                  'password': password})


class Config(object):
    # Statement for enabling the development environment
    DEBUG = False
    TESTING = False

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Define the application directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    #UPLOAD_FOLDER = os.path.join(BASE_DIR, 'media')

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    DATABASE_CONNECT_OPTIONS = {}

    # Enable protection against *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    host = 'db.prof'
    username = 'pfuser'
    password = 'min~Kovski'

    # Secret key for signing cookies
    SECRET_KEY = '(sd0f@r^&37#W0y!kf<5'

    # Facebook settings
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''


class ProductionDevelopmentConfig(Config):

    #Define database connection parameters
    host = os.getenv('PRODUCTION_SERVER_DB_HOST', Config.host)
    username = os.getenv('PRODUCTION_SERVER_DB_USERNAME', Config.username)
    password = os.getenv('PRODUCTION_SERVER_DB_PASSWORD', Config.password)
    db_name = os.getenv('PRODUCTION_SERVER_DB_NAME', 'profireader')

    # Define production database
    SQLALCHEMY_DATABASE_URI = \
        database_uri(host, username, password, db_name)

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = os.getenv('PRODUCTION_SERVER_CSRF_SESSION_KEY', None)

    # Secret key for signing cookies
    SECRET_KEY = os.getenv('PRODUCTION_SERVER_SECRET_KEY', Config.SECRET_KEY)

    SITE_TITLE = os.getenv('PRODUCTION_SERVER_SITE_TITLE', 'Profireader')

    # Facebook settings
    CONSUMER_KEY = os.getenv('PRODUCTION_SERVER_CONSUMER_KEY',
                             Config.CONSUMER_KEY)
    CONSUMER_SECRET = os.getenv('PRODUCTION_SERVER_CONSUMER_SECRET',
                                Config.CONSUMER_SECRET)

    if 'PRODUCTION_SERVER_DB_HOST' not in os.environ.keys():

        # Statement for enabling the development environment
        DEBUG = True

        # Enable protection against *Cross-site Request Forgery (CSRF)*
        CSRF_ENABLED = False


class TestingConfig(Config):
    # Statement for enabling the development environment
    DEBUG = True
    TESTING = True

    # Disable protection against *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = False

    #Define database connection parameters
    db_name = 'profireader_test'

    # Define the database - we are working with
    SQLALCHEMY_DATABASE_URI = \
        database_uri(Config.host, Config.username, Config.password, db_name)

    # Secret key for signing cookies
    SECRET_KEY = Config.SECRET_KEY

    SITE_TITLE = "TEST"

    # Facebook settings
    CONSUMER_KEY = Config.CONSUMER_KEY
    CONSUMER_SECRET = Config.CONSUMER_SECRET
