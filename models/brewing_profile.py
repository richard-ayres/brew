import enum

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship, backref

from .base import Base


class RecipeType(enum.Enum):
    all_grain = 1
    extract = 2


class SpargeMethod(enum.Enum):
    fly_sparge = 1
    batch_sparge = 2
    brew_in_a_bag = 3


class BrewingProfile(Base):
    __tablename__ = 'brew_profiles'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # All volumes in litres
    volume_before_boil = Column(Float, nullable=False)
    volume_after_boil = Column(Float, nullable=False)
    volume_transferred = Column(Float, nullable=False)  # vol transferred into fermenter

    volume_added_to_fermenter = Column(Float, nullable=False)
    volume_in_fermenter = Column(Float, nullable=False) # vol in fermenter, i.e. vol_transferred+vol_added

    volume_final = Column(Float, nullable=False)    # vol of finished beer

    boil_duration = Column(Float, nullable=False)   # usual boil duration in minutes

    recipe_type = Column(Enum(RecipeType), nullable=False)
    mash_schedule_id = Column(Integer, ForeignKey('mash_schedules.id'), nullable=True)
    mash_schedule = relationship('MashSchedule')
    sparge_method = Column(Enum(SpargeMethod), nullable=True)

    base_water_id = Column(Integer, ForeignKey('waters.id'), nullable=True)
    base_water = relationship('Water', foreign_keys=[base_water_id])
    target_water_id = Column(Integer, ForeignKey('waters.id'), nullable=True)
    target_water = relationship('Water', foreign_keys=[target_water_id])

    mash_tun_thermal_mass = Column(Float, nullable=True, default=1.0)    # in kg
    mash_ratio = Column(Float, nullable=True, default=2.5)   # water:grain ratio in litres per kg
    mash_efficiency = Column(Float, nullable=True, default=0.75)
