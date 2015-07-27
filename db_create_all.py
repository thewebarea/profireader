from db_init import Base, engine

def create_all_tables():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import all_models
    Base.metadata.create_all(bind=engine)

create_all_tables()
