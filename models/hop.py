from sqlalchemy import Column, Integer, String, Float

from .base import Base


class Hop(Base):
    __tablename__ = 'hops'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    alpha = Column(Float, nullable=False)