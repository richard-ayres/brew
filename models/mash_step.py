import enum

from sqlalchemy import Column, Integer, Float, ForeignKey, String, Enum
from sqlalchemy.orm import relationship, backref

from .base import Base


class StepType(enum.Enum):
    rest = 1
    raise_by_infusion = 2
    boil_decoction = 3          # Pull decoction, boil, add, raising mash to
    raise_by_direct_heat = 4
    raise_to_and_mash_out = 5


class MashStep(Base):
    __tablename__ = 'mash_steps'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=True)

    type = Column(Enum(StepType), nullable=False)
    temperature = Column(Float, nullable=False)     # in Celsius
    duration = Column(Integer, nullable=False)      # in minutes

    next_step_id = Column(Integer, ForeignKey('mash_steps.id', ondelete='CASCADE'), nullable=True)
    next_step = relationship('MashStep', backref=backref('prev_step', uselist=False))
