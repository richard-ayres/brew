from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base, UUID


class UserRecipeLink(Base):
    __tablename__ = 'user_recipes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    recipe_id = Column(UUID, ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    writable = Column(Boolean, nullable=False, default='1')

    user = relationship('User')
    recipe = relationship('Recipe')
