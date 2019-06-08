from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class GrainBill(Base):
    __tablename__ = 'grain_bill'

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipe.id'), nullable=False)
    fermentable_id = Column(Integer, ForeignKey('fermentables.id'), nullable=False)
    weight = Column(Float, nullable=False)  # comment="Weight of fermentable in grams")
    ebc = Column(Float, nullable=True)  # comment="Override default EBC")
    extract_max = Column(Float, nullable=True)  # comment="Override default extract")
    fermentability = Column(Float, nullable=True)   # comment="Override default fermentability")

    fermentable = relationship('Fermentable')

    def __repr__(self):
        return "Grain bill item: {fermentable} @{weight}g (EBC={ebc}, Extract={extract}, Fermentability={fermentability})".format(
            fermentable=(self.fermentable.name if self.fermentable else 'Unknown'),
            weight=self.weight,
            ebc=(self.ebc if self.ebc is not None else 'inherited'),
            extract=(self.extract_max if self.extract_max is not None else 'inherited'),
            fermentability=(self.fermentability if self.fermentability is not None else 'inherited'),
        )