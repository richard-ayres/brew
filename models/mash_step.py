import enum

from sqlalchemy import Column, Integer, Float, ForeignKey, String, Enum
from sqlalchemy.orm import relationship, backref

from database import Base


class StepType(str, enum.Enum):
    rest: str = 'rest'
    raise_by_infusion: str = 'raise_by_infusion'
    boil_decoction: str = 'boil_decoction'          # Pull decoction, boil, add, raising mash to
    raise_by_direct_heat: str = 'raise_by_direct_heat'
    raise_to_and_mash_out: str = 'raise_to_and_mash_out'


class MashStep(Base):
    __tablename__ = 'mash_steps'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=True)

    type = Column(Enum(StepType), nullable=False)
    temperature = Column(Float, nullable=False)     # in Celsius
    duration = Column(Integer, nullable=False)      # in minutes

    next_step_id = Column(Integer, ForeignKey('mash_steps.id', ondelete='CASCADE'), nullable=True)
    next_step = relationship('MashStep')
