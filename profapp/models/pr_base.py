from db_init import db_session
from sqlalchemy import Table, Column, Integer, Text, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, backref, make_transient, class_mapper
from sqlalchemy.types import DateTime
import datetime
from flask.ext.login import current_user, login_required


class PRBase:
    @login_required
    def save(self):
        # p = Parent()  # current_user
        # a = Association(extra_data="some data")  # CompanyUser
        # a.child = Child()
        # p.children.append(a)
        #
        # # iterate through child objects via association, including association
        # # attributes
        # for assoc in p.children:
        #     print assoc.extra_data
        #     print assoc.child

        db_session.add(self)
        # db_session.flush()
        db_session.commit()
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

    def dict(self, found=None):
        if found is None:
            found = set()
        mapper = class_mapper(self.__class__)
        columns = [column.key for column in mapper.columns]
        get_key_value = lambda c: (c, getattr(self, c).isoformat()) if isinstance(getattr(self, c),
                                                                                  datetime.datetime) else (
        c, getattr(self, c))
        # get_key_value = lambda c: (c, getattr(self, c).__str__)
        out = dict(map(get_key_value, columns))
        for name, relation in mapper.relationships.items():
            if relation not in found:
                found.add(relation)
                related_obj = getattr(self, name)
                if related_obj is not None:
                    if relation.uselist:
                        out[name] = [child.dict(found) for child in related_obj]
                    else:
                        out[name] = related_obj.dict(found)
        return out

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
