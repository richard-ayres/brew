from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from database import Base


class MashSchedule(Base):
    __tablename__ = 'mash_schedules'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)

    first_step_id = Column(Integer, ForeignKey('mash_steps.id', ondelete='CASCADE'), nullable=False)
    first_step = relationship('MashStep', backref=backref('prev_step', uselist=False))
