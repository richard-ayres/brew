import enum

from sqlalchemy import Column, Float, String, Enum

from database import Base, UUID, uuidgen


class FlocculationLevel(str, enum.Enum):
    low: str = 'low'
    medium: str = 'medium'
    high: str = 'high'


class YeastType(str, enum.Enum):
    dry: str = 'dry'
    liquid: str = 'liquid'


class BeerType(str, enum.Enum):
    ale: str = 'ale'
    lager: str = 'lager'


class Yeast(Base):
    __tablename__ = 'yeasts'

    id = Column(UUID, primary_key=True, default=uuidgen)
    name = Column(String(128), nullable=False)

    attenuation = Column(Float, nullable=False)     # attenuation, 0.0 -> 1.0
    flocculation = Column(Enum(FlocculationLevel), nullable=False, default='medium')
    type = Column(Enum(YeastType), nullable=False, default='dry')
    beer_type = Column(Enum(BeerType), nullable=False, default='ale')
