from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base, UUID


class UserBatchLink(Base):
    __tablename__ = 'user_batches'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    batch_id = Column(UUID, ForeignKey('batches.id', ondelete='CASCADE'), nullable=False)
    writable = Column(Boolean, nullable=False, default='1')

    user = relationship('User')
    batch = relationship('Batch')
