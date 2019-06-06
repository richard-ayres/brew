import enum

from sqlalchemy import Column, Integer, Float, String, Enum
from sqlalchemy.orm import relationship, backref

from .base import Base


class FlocculationLevel(enum.Enum):
    low = 1
    medium = 2
    high = 3


class YeastType(enum.Enum):
    dry = 1
    liquid = 2


class BeerType(enum.Enum):
    ale = 1
    lager = 2


class Yeast(Base):
    __tablename__ = 'yeast'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)

    attenuation = Column(Float, nullable=False)     # attenuation, 0.0 -> 1.0
    flocculation = Column(Enum(FlocculationLevel), nullable=False)
    type = Column(Enum(YeastType), nullable=False, default='dry')
    beer_type = Column(Enum(BeerType), nullable=False, default='ale')
