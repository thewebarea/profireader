from db_init import db_session, Base
from sqlalchemy import Table, Column, Integer, Text, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, backref, make_transient, class_mapper
import datetime
import re


class PRBase():
    def save(self):
        db_session.add(self)
        db_session.flush()
        return self

    def attr(self, dictionary):
        for k in dictionary:
            setattr(self, k, dictionary[k]);
        return self

    def detach(self):
        db_session.expunge(self)
        make_transient(self)
        self.id = None
        return self




        #
        # if found is None:
        #     found = []
        # if found_converted is None:
        #     found_converted = []
        # mapper = class_mapper(self.__class__)
        # columns = [column.key for column in mapper.columns]
        # get_key_value = lambda c: (c, getattr(self, c).isoformat()) if isinstance(getattr(self, c),
        #                                                                           datetime.datetime) else (
        # c, getattr(self, c))
        # # get_key_value = lambda c: (c, getattr(self, c).__str__)
        # out = dict(map(get_key_value, columns))
        # for name, relation in mapper.relationships.items():
        #     if relation.uselist:
        #         if relation not in found:
        #             found.append(relation)
        #             found_converted.append(True)
        #             found_index = len(found_converted)-1
        #             related_obj = getattr(self, name)
        #             converted = [child.dict(found, found_converted) for child in related_obj] if relation.uselist else related_obj.dict(found, found_converted)
        #             found_converted[found_index] = converted
        #             if related_obj is not None:
        #                 out[name] = converted
        #         else:
        #             out[name] = found_converted[found.index(relation)]
        #     else:
        #         converted = related_obj.dict(found, found_converted)
        #         if related_obj is not None:
        #                 out[name] = converted
        # return out

    @classmethod
    def get(cls, id):
        return db_session().query(cls).get(id)


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
                        req_relationships[column_name].append('.'.join(columnsdevided))

        # req_columns = list(set(req_columns))
        # req_relationships = {relationname:convert_col_to_arrays(*nextlevelcols) for relationname,nextlevelcols in relationships}

        columns = class_mapper(self.__class__).columns
        realations = {a:b for (a,b) in  class_mapper(self.__class__).relationships.items()}

        get_key_value = lambda o: o.isoformat() if isinstance(o, datetime.datetime) else o
        for col in columns:
            if col.key in req_columns or '*' in req_columns:
                ret[col.key] = get_key_value(getattr(self, col.key))
                if col.key in req_columns:
                    del req_columns[col.key]
        if '*' in req_columns:
            del req_columns['*']

        if len(req_columns) > 0:
            columns_not_in_relations = list(set(req_columns.keys()) - set(realations.keys()))
            if len(columns_not_in_relations) > 0:
                raise ValueError(
                    "you requested not existing attribute(s) `%s%s`" % (prefix, '`, `'.join(columns_not_in_relations),))
            else:
                raise ValueError("you requested for attribute(s) but relationships found `%s%s`" % (
                prefix, '`, `'.join(set(realations.keys()).intersection(req_columns.keys())),))

        for relationname, relation in realations.items():
            if relationname in req_relationships or '*' in req_relationships:
                if relationname in req_relationships:
                    nextlevelargs = req_relationships[relationname]
                    del req_relationships[relationname]
                else:
                    nextlevelargs = req_relationships['*']
                related_obj = getattr(self, relationname)
                if relation.uselist:
                    ret[relationname] = [child.to_dict(*nextlevelargs, prefix = prefix + relationname + '.') for child in
                                         related_obj]
                else:
                    ret[relationname] = related_obj.to_dict(*nextlevelargs, prefix = prefix + relationname + '.')

        if '*' in req_relationships:
            del req_relationships['*']

        if len(req_relationships) > 0:
            relations_not_in_columns = list(set(req_relationships.keys()) - set(columns))
            if len(relations_not_in_columns) > 0:
                raise ValueError(
                    "you requested not existing relation(s) `%s%s`" % (prefix, '`, `'.join(relations_not_in_columns),))
            else:
                raise ValueError("you requested for relation(s) but column(s) found `%s%s`" % (
                prefix, '`, `'.join(set(columns).intersection(req_relationships)),))

        return ret

    # @staticmethod
    # def searchResult(collection, convert_item = lambda item: item.dict()):
    #     ret = {}
    #     for x in collection:
    #         ret[x.id] = convert_item(x)
    #
    #     return ret

