from sqlalchemy import Column, Integer, Float, String

from .base import Base


class Water(Base):
    __tablename__ = 'waters'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)

    # All figures in ppm
    calcium = Column(Float, nullable=False)
    bicarbonate = Column(Float, nullable=False)
    sulphate = Column(Float, nullable=False)
    chloride = Column(Float, nullable=False)
    sodium = Column(Float, nullable=False)
    magnesium = Column(Float, nullable=False)
