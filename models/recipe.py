from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, backref

from .base import Base


class Recipe(Base):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    profile_id = Column(Integer, ForeignKey('brew_profiles.id'))

    profile = relationship('BrewingProfile', backref='recipes')
    grain_bill = relationship('GrainBill', backref=backref('recipe', uselist=False))
    hop_schedule = relationship('HopSchedule', backref=backref('recipe', uselist=False))