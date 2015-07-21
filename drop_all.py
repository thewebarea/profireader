from profapp import models
from db_connect import metadata, engine

metadata.drop_all(engine)
