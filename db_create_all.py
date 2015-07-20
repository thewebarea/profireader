from database import Base, engine

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import profapp.models.users
    import profapp.models.company
    import profapp.models.articles
    Base.metadata.create_all(bind=engine)

init_db()
