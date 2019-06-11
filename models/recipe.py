from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from database import Base, UUID, uuidgen


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(UUID, primary_key=True, default=uuidgen)

    name = Column(String(128), nullable=False)
    profile_id = Column(UUID, ForeignKey('brew_profiles.id'))
    yeast_id = Column(UUID, ForeignKey('yeasts.id'), nullable=True)

    profile = relationship('BrewingProfile', backref='recipes')
    grain_bill = relationship('GrainBill', backref=backref('recipe', uselist=False))
    hop_schedule = relationship('HopSchedule', backref=backref('recipe', uselist=False))
    yeast = relationship('Yeast')