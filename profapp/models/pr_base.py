
from db_init import db_session
from sqlalchemy import Table, Column, Integer, Text, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, backref, make_transient

class PRBase():

    def save(self):
        db_session.add(self)
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

    @classmethod
    def get(cls, id):
        return db_session().query(cls).filter_by(id=id).one()

