from sqlalchemy import Column, Float, String

from database import Base, UUID, uuidgen


class Water(Base):
    __tablename__ = 'waters'

    id = Column(UUID, primary_key=True, default=uuidgen)
    name = Column(String(128), nullable=False)

    # All figures in ppm
    calcium = Column(Float, nullable=False)
    bicarbonate = Column(Float, nullable=False)
    sulphate = Column(Float, nullable=False)
    chloride = Column(Float, nullable=False)
    sodium = Column(Float, nullable=False)
    magnesium = Column(Float, nullable=False)
