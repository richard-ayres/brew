from sqlalchemy import Column, String, Float, Boolean

from database import Base, UUID, uuidgen


class Fermentable(Base):
    __tablename__ = 'fermentables'

    id = Column(UUID, primary_key=True, default=uuidgen)
    name = Column(String, unique=True, nullable=False)
    extract_max = Column(Float, nullable=False)
    ebc = Column(Float, nullable=False)
    fermentability = Column(Float, default=0.62)
    is_extract = Column(Boolean, default=False)
    requires_mash = Column(Boolean, default=True)