from db_init import db_session


def db(arg, **kwargs):
    return db_session.query(arg).filter_by(**kwargs)
