from sqlalchemy import Column, String, Float

from database import Base, UUID, uuidgen


class Hop(Base):
    __tablename__ = 'hops'

    id = Column(UUID, primary_key=True, default=uuidgen)
    name = Column(String, unique=True, nullable=False)
    alpha = Column(Float, nullable=False)