from calculators import Fermentable as FermentableCalculator
from models import Fermentable as FermentableModel


class Fermentable(FermentableCalculator):

    @classmethod
    def from_model(cls, model):
        return cls(**model.__dict__)

    def to_model(self):
        kmap = lambda key: key.replace('-', '_')
        model = FermentableModel()
        model.__dict__.update({kmap(k):self.params[k] for k in self.params.keys()})
        return model
