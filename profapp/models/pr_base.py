# from db_init import g.db, Base
from ..constants.TABLE_TYPES import TABLE_TYPES
from sqlalchemy import Table, Column, Integer, Text, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, backref, make_transient, class_mapper
import datetime
import re
from flask import g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import event
from utils.validators import validators
from ..controllers import errors
from utils.db_utils import db


Base = declarative_base()

# this event is called whenever an attribute
# on a class is instrumented
# @event.listens_for(Base, 'attribute_instrument')
# def configure_listener(class_, key, inst):
#     if not hasattr(inst.property, 'columns'):
#         return
#     # this event is called whenever a "set"
#     # occurs on that instrumented attribute
#
#     @event.listens_for(inst, "set", retval=True)
#     def set_(instance, value, oldvalue, initiator):
#         validator = validators.get(inst.property.columns[0].type.__class__)
#         if validator:
#             return validator(value)
#         else:
#             return value
class Search(Base):
    __tablename__ = 'search'
    id = Column(TABLE_TYPES['id_profireader'], nullable=False, primary_key=True, unique=True)
    index = Column(TABLE_TYPES['id_profireader'], nullable=False)
    table_name = Column(TABLE_TYPES['short_text'], nullable=False)
    text = Column(TABLE_TYPES['text'], nullable=False)
    relevance = Column(TABLE_TYPES['int'], nullable=False)
    kind = Column(TABLE_TYPES['short_text'])

    def __init__(self, index=None, table_name=None, text=None, relevance=None, kind=None):
        super(Search, self).__init__()
        self.index = index
        self.table_name = table_name
        self.text = text
        self.relevance = relevance
        self.kind = kind

    @staticmethod
    def get_relevance(field_name):
        rel = {'keywords': 10, 'title': 9, 'name': 8, 'short': 7, 'long_stripped': 6}
        return rel[field_name]

class PRBase:
    def __init__(self):
        self.query = g.db.query_property()

    def validate(self, action):
        return {'errors': {}, 'warnings': {}, 'notices': {}}

    def delfile(self):
        g.db.delete(self)
        g.db.commit()

    def save(self):
        g.db.add(self)
        g.db.flush()
        return self

    def updates(self, dictionary):
        for f in dictionary:
            setattr(self, f, dictionary[f])
        return self

    def attr(self, dictionary):
        for k in dictionary:
            setattr(self, k, dictionary[k])
        return self

    def detach(self):
        g.db.expunge(self)
        make_transient(self)
        self.id = None
        return self

    def expunge(self):
        g.db.expunge(self)
        return self

    def get_client_side_dict(self, fields='id'):
        return self.to_dict(fields)

    @classmethod
    def get(cls, id):
        return g.db().query(cls).get(id)

# TODO: OZ by OZ:**kwargs should accept lambdafunction for fields formattings
    def to_dict(self, *args, prefix=''):
        ret = {}

        req_columns = {}
        req_relationships = {}

        for arguments in args:
            for argument in re.compile('\s*,\s*').split(arguments):
                columnsdevided = argument.split('.')
                column_names = columnsdevided.pop(0)
                for column_name in column_names.split('|'):
                    if len(columnsdevided) == 0:
                        req_columns[column_name] = True
                    else:
                        if column_name not in req_relationships:
                            req_relationships[column_name] = []
                        req_relationships[column_name].append(
                            '.'.join(columnsdevided))

        columns = class_mapper(self.__class__).columns
        relations = {a: b for (a, b) in class_mapper(self.__class__).relationships.items()}

        get_key_value = lambda o: o.strftime('%c') if isinstance(
            o, datetime.datetime) else o
        for col in columns:
            if col.key in req_columns or '*' in req_columns:
                ret[col.key] = get_key_value(getattr(self, col.key))
                if col.key in req_columns:
                    del req_columns[col.key]
        if '*' in req_columns:
            del req_columns['*']

        if len(req_columns) > 0:
            columns_not_in_relations = list(set(req_columns.keys()) - set(relations.keys()))
            if len(columns_not_in_relations) > 0:
                raise ValueError(
                    "you requested not existing attribute(s) `%s%s`" % (
                        prefix, '`, `'.join(columns_not_in_relations),))
            else:
                raise ValueError("you requested for attribute(s) but "
                                 "relationships found `%s%s`" % (
                    prefix, '`, `'.join(set(relations.keys()).
                                        intersection(
                            req_columns.keys())),))

        for relationname, relation in relations.items():
            if relationname in req_relationships or '*' in \
                    req_relationships:
                if relationname in req_relationships:
                    nextlevelargs = req_relationships[relationname]
                    del req_relationships[relationname]
                else:
                    nextlevelargs = req_relationships['*']
                related_obj = getattr(self, relationname)
                if relation.uselist:
                    ret[relationname] = [
                        child.to_dict(*nextlevelargs,
                                      prefix=prefix + relationname + '.'
                                      ) for child in
                                         related_obj]
                else:
                    ret[relationname] = None if related_obj is None else related_obj.to_dict(*nextlevelargs, prefix=prefix + relationname + '.')

        if '*' in req_relationships:
            del req_relationships['*']

        if len(req_relationships) > 0:
            relations_not_in_columns = list(set(
                req_relationships.keys()) - set(columns))
            if len(relations_not_in_columns) > 0:
                raise ValueError(
                    "you requested not existing relation(s) `%s%s`" % (
                        prefix, '`, `'.join(relations_not_in_columns),))
            else:
                raise ValueError("you requested for relation(s) but "
                                 "column(s) found `%s%s`" % (
                    prefix, '`, `'.join(set(columns).intersection(
                        req_relationships)),))

        return ret

    @staticmethod
    def validate_before_update(mapper, connection, target):
        ret = target.validate('update')
        if len(ret['errors'].keys()):
            raise errors.ValidationException(ret)

    @staticmethod
    def validate_before_insert(mapper, connection, target):
        ret = target.validate('insert')
        if len(ret['errors'].keys()):
            raise errors.ValidationException(ret)

    # @staticmethod
    # def validate_before_delete(mapper, connection, target):
    #     ret = target.validate('delete')
    #     if len(ret['errors'].keys()):
    #         raise errors.ValidationException(ret)

    @staticmethod
    def add_to_search(mapper, connection, target):

        if hasattr(target, 'search_fields'):
            if not target.id:
                target.save()
            add_to_db = []
            for field in target.search_fields:
                search_setter = Search(index=target.id, table_name=target.__tablename__,
                                       relevance=Search.get_relevance(field), kind=field)
                setattr(search_setter, 'text', getattr(target, field))
                add_to_db.append(search_setter)
            g.db.add_all(add_to_db)

    @staticmethod
    def update_search_table(mapper, connection, target):
        if hasattr(target, 'search_fields'):
            for field in target.search_fields:
                db(Search, index=target.id, kind=field).update({'text': getattr(target, field)})

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, 'before_update', cls.validate_before_update)
        event.listen(cls, 'before_insert', cls.validate_before_insert)
        # event.listen(cls, 'before_delete', cls.validate_before_delete)
        event.listen(cls, 'after_insert', cls.add_to_search)
        event.listen(cls, 'before_update', cls.update_search_table)

#
#
#
#
# @event.listens_for(PRBase, 'before_insert')
# def validate_insert(mapper, connection, target):
#     ret = target.validate('insert')
#     if len(ret['errors'].keys()):
#         raise errors.ValidationException(ret)
#
# @event.listens_for(PRBase, 'before_delete')
# def validate_delete(mapper, connection, target):
#     ret = target.validate('delete')
#     if len(ret['errors'].keys()):
#         raise errors.ValidationException(ret)
#
# @event.listens_for(PRBase, 'before_update')
# def validate_update(mapper, connection, target):
#     ret = target.validate('update')
#     if len(ret['errors'].keys()):
#         raise errors.ValidationException(ret)
#
# event.listen(PRBase, 'before_update', validate_update)
# event.listen(ArticlePortal, 'before_insert', set_long_striped)
# event.listen(ArticleCompany, 'before_update', set_long_striped)
# event.listen(ArticleCompany, 'before_insert', set_long_striped)
