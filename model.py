# 3rd
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, BigInteger
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

Base = declarative_base()


class Questionnaire(Base):
    __tablename__ = 'Questionnaires'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    version = Column(Integer)
    author = Column(String)
    created = Column(DateTime)