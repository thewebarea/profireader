from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import ProductionDevelopmentConfig

engine = create_engine(ProductionDevelopmentConfig.SQLALCHEMY_DATABASE_URI,
                       echo=True)
metadata = MetaData()
sql_session = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=engine))
