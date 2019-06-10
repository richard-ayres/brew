from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base, UUID


class UserProfileLink(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    profile_id = Column(UUID, ForeignKey('brew_profiles.id', ondelete='CASCADE'), nullable=False)
    writable = Column(Boolean, nullable=False, default='1')

    user = relationship('User')
    profile = relationship('BrewingProfile')
