from flask import g


def db(*args, **kwargs):
    return g.db.query(*args).filter_by(**kwargs)
