from calculators import Fermentable as FermentableCalculator
from models import Fermentable as FermentableModel

class Fermentable(FermentableCalculator):

    @staticmethod
    def from_model(model):
        return Fermentable(**model.__dict__)

    def to_model(self):
        kmap = lambda key: key.replace('-', '_')
        model = FermentableModel()
        model.__dict__.update({kmap(k):self.params[k] for k in self.params.keys()})
        return model
