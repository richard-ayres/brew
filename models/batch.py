from sqlalchemy import Column, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship

from database import Base, UUID, uuidgen


class Batch(Base):
    __tablename__ = 'batches'

    id = Column(UUID, primary_key=True, default=uuidgen)

    recipe_id = Column(String(36), ForeignKey('recipes.id', ondelete='SET NULL'), nullable=True)
    recipe = relationship('Recipe', backref='batches')

    brew_date = Column(DateTime, nullable=True)
    rack_date = Column(DateTime, nullable=True)
    package_date = Column(DateTime, nullable=True)

    # Actuals
    profile_id = Column(String(36), ForeignKey('brew_profiles.id', ondelete='RESTRICT'))
    actual_profile = relationship('BrewingProfile', foreign_keys=[profile_id])

    pre_boil_gravity = Column(Float, nullable=True)
    original_gravity = Column(Float, nullable=True)
    final_gravity = Column(Float, nullable=True)

