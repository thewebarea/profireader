from sqlalchemy import MetaData,create_engine
from sqlalchemy.orm import sessionmaker

metadata=MetaData()
engine = create_engine('postgresql://postgres:minkovski@postgres.d/Profireader')
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
sql_session=Session()
