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


def map_yeast_params(params):
    """Clean up yeast data"""
    def do_map_yeast_params(key, value):
        if key == 'name':
            return str(value).encode('utf-8')

        if str(value).lower() == 'na':
            return None

        if key == 'attenuation' and not isinstance(value, float) and not isinstance(value, int):
            value = 0.7 if value.lower() == 'low' else \
                    0.75 if value.lower() in {'med', 'medium'} else \
                    0.8
            if value > 1.0:
                value = value / 100.0

            return value

        if key == 'flocculation':
            if value.lower() == 'med':
                return 'medium'
            if value.lower() == 'med/high':
                return 'high'
            if value.lower() == 'very high':
                return 'high'

        if key == 'type':
            if value == 'dried':
                return 'dry'

        return value

    return {key: do_map_yeast_params(key, value) for key, value in params.items()}


class Yeast(Base):
    __tablename__ = 'yeasts'

    def __init__(self, **kwargs):
        super().__init__(**map_yeast_params(kwargs))

    id = Column(UUID, primary_key=True, default=uuidgen)
    name = Column(String(128), nullable=False)

    attenuation = Column(Float, nullable=False)     # attenuation, 0.0 -> 1.0
    flocculation = Column(Enum(FlocculationLevel), nullable=False, default='medium')
    type = Column(Enum(YeastType), nullable=False, default='dry')
    beer_type = Column(Enum(BeerType), nullable=False, default='ale')

    # max and min temperatures in C
    temp_min = Column(Float, nullable=True)
    temp_max = Column(Float, nullable=True)
