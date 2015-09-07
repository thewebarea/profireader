from flask import g


def db(arg, **kwargs):
    return g.db.query(arg).filter_by(**kwargs)
