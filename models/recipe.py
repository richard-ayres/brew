from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from database import Base, UUID, uuidgen


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(UUID, primary_key=True, default=uuidgen)

    name = Column(String(128), nullable=False)
    profile_id = Column(UUID, ForeignKey('brew_profiles.id'))

    profile = relationship('BrewingProfile', backref='recipes')
    grain_bill = relationship('GrainBill', backref=backref('recipe', uselist=False))
    hop_schedule = relationship('HopSchedule', backref=backref('recipe', uselist=False))