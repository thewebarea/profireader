from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from config import ProductionDevelopmentConfig
#from profapp import create_app

# see this: http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/
# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
engine = create_engine(ProductionDevelopmentConfig.SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
