import enum

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship

from database import Base, UUID


class HopWhen(str, enum.Enum):
    fwh: str = 'fwh'
    boil: str = 'boil'
    whirlpool: str = 'whirlpool'
    fermenter: str = 'fermenter'
    dry: str = 'dry'


class HopSchedule(Base):
    __tablename__ = 'hop_schedule'

    id = Column(Integer, primary_key=True)
    recipe_id = Column(UUID, ForeignKey('recipes.id'), nullable=False)
    hop_id = Column(UUID, ForeignKey('hops.id'), nullable=False)
    weight = Column(Float, nullable=False)  # "Weight of hop in grams")
    alpha = Column(Float, nullable=True)    # "Override default alpha value")
    when = Column(Enum(HopWhen), nullable=False)
    boil_time = Column(Integer, nullable=True)  # "How long to boil, in minutes, for 'when' is 'boil', 'fwh' or 'whirlpool'")

    hop = relationship('Hop')
