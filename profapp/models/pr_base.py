from db_init import db_session, Base
from sqlalchemy import Table, Column, Integer, Text, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, backref, make_transient, class_mapper
import datetime


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

    # @staticmethod
    # def searchResult(collection, convert_item = lambda item: item.dict()):
    #     ret = {}
    #     for x in collection:
    #         ret[x.id] = convert_item(x)
    #
    #     return ret

