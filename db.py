#!/Users/andersaarvikBC/PycharmProjects/webdl/bin/python

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, \
    DateTime, \
    String, \
    Integer, \
    ForeignKey, \
    select

Base = declarative_base()


class Website(Base):
    __tablename__ = 'website'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    last_modified = Column(DateTime)


class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)
    website_id = Column(String, ForeignKey('website.url'))
    type = Column(String)
    output = Column(String)
    timestamp = Column(DateTime)


class Options(Base):
    __tablename__ = 'options'
    id = Column(Integer, primary_key=True)
    option = Column(String)
    option_type = Column(String)
    option_value = Column(String)

from sqlalchemy import create_engine
engine = create_engine('sqlite:////Users/andersaarvikBC/Desktop/webdl/webdl/webdl.db')

from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
