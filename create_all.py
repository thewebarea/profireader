from profapp import models
from db_connect import metadata, engine, sql_session
from profapp.models.company import Company
from profapp.models.users import User, mapper
from profapp.models.articles import ArticleHistory
from profapp.models.files import Files

#sql_session.add(Company('Robota'))
#sql_session.commit()

metadata.create_all(engine)
