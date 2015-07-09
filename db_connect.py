from sqlalchemy import MetaData,create_engine
from sqlalchemy.orm import sessionmaker,scoped_session

metadata=MetaData()
engine = create_engine('postgresql://postgres:minkovski@postgres.d/Profireader')
sql_session=scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
def init_db():
    metadata.create_all(bind=engine)