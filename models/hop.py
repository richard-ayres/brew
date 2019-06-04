from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Hop(Base):
    __tablename__ = 'hops'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    alpha = Column(Float, nullable=False)