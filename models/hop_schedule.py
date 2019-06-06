import enum

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship

from .base import Base


class HopWhen(enum.Enum):
    fwh = 1
    boil = 2
    whirlpool = 3
    fermenter = 4
    dry = 5


class HopSchedule(Base):
    __tablename__ = 'hop_schedule'

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipe.id'), nullable=False)
    hop_id = Column(Integer, ForeignKey('hops.id'), nullable=False)
    weight = Column(Float, nullable=False)  # "Weight of hop in grams")
    alpha = Column(Float, nullable=True)    # "Override default alpha value")
    when = Column(Enum(HopWhen), nullable=False)
    boil_time = Column(Integer, nullable=True)  # "How long to boil, in minutes, for 'when' is 'boil', 'fwh' or 'whirlpool'")

    hop = relationship('Hop')
