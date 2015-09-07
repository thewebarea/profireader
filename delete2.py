from flask import Flask, render_template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from config import ProductionDevelopmentConfig
from sqlalchemy import event
from utils.validators import validators

import os

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


def database_uri(host, username, password, db_name):
    return 'postgresql+psycopg2://{username}:{password}@{host}/{db_name}'. \
        format(**{'db_name': db_name,
                  'host': host,
                  'username': username,
                  'password': password})


host = 'localhost'
username = 'flasky_user'
password = 'FH$7b)4~g7fG5&!`hG]fg'
db_name = 'SQLAlchemyTest'


SQLALCHEMY_DATABASE_URI = \
    database_uri(host, username, password, db_name)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()

# this event is called whenever an attribute
# on a class is instrumented
@event.listens_for(Base, 'attribute_instrument')
def configure_listener(class_, key, inst):
    if not hasattr(inst.property, 'columns'):
        return
    # this event is called whenever a "set"
    # occurs on that instrumented attribute

    @event.listens_for(inst, "set", retval=True)
    def set_(instance, value, oldvalue, initiator):
        validator = validators.get(inst.property.columns[0].type.__class__)
        if validator:
            return validator(value)
        else:
            return value

Base.query = db_session.query_property()


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # employees = relationship(
    #     'Employee',
    #     secondary='department_employee_link',
    #     lazy='dynamic'
    # )


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hired_on = Column(DateTime, default=func.now())
    departments = relationship(
        Department,
        secondary='department_employee_link'
    )


class DepartmentEmployeeLink(Base):
    __tablename__ = 'department_employee_link'
    department_id = Column(Integer, ForeignKey('department.id'), primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    extra_data = Column(String(256))
    department = relationship(Department, backref=backref("employee_assoc"))
    employee = relationship(Employee, backref=backref("department_assoc"))

#Base.metadata.drop_all(bind=engine)
#Base.metadata.create_all(bind=engine)

department1 = Department(name='IT')
department2 = Department(name='Sale')
employee1 = Employee(name='Andriy')
employee2 = Employee(name='Victor')

db_session.add(employee1)
db_session.commit()


#it works!!!
DepartmentEmployee = DepartmentEmployeeLink(extra_data='useful experiments')
DepartmentEmployee.department = department1
employee1.department_assoc.append(DepartmentEmployee)

db_session.add(employee1)
db_session.commit()

# it works!!!
# DepartmentEmployee = DepartmentEmployeeLink(extra_data='some info')
# DepartmentEmployee.department = department1
# employee1.department_assoc.append(DepartmentEmployee)
#
# db_session.add(employee1)
# db_session.commit()


# it works!!!
# DepartmentEmployee = DepartmentEmployeeLink(extra_data='some info')
# department1.employee_assoc.append(DepartmentEmployee)
# employee1.department_assoc.append(DepartmentEmployee)
#
# db_session.add(DepartmentEmployee)
# db_session.commit()


# it works!!!
# DepartmentEmployee = DepartmentEmployeeLink(extra_data='some info')
# DepartmentEmployee.department = department1
# DepartmentEmployee.employee = employee1
#
# db_session.add(DepartmentEmployee)
# db_session.commit()


# IT DOESN'T WORK!!!
# DepartmentEmployee = DepartmentEmployeeLink(extra_data='some info')
# department1.employee_assoc.append(DepartmentEmployee)
# employee1.departments.append(department1)
#
# db_session.add(employee1)
# db_session.commit()

#employee1 = db_session.query(Employee).filter_by(id=1).first()


print('pause')
print('OK')


# # **************************************************************

#  app = Flask(__name__)

# if __name__ == '__main__':
#    app.run()
