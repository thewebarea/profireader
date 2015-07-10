from sqlalchemy import MetaData,create_engine
from sqlalchemy.orm import sessionmaker,scoped_session


engine = create_engine('postgresql://postgres:minkovski@postgres.d/Profireader',echo=True)
metadata=MetaData()
sql_session=scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

