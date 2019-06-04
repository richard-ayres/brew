from calculators import HopAddition as HopCalculator
from models import Hop as HopModel


class Hop(HopCalculator):

    @classmethod
    def from_model(cls, model):
        return cls(**model.__dict__)

    def to_model(self):
        kmap = lambda key: key.replace('-', '_')
        model = HopModel()
        model.__dict__.update({kmap(k):self.params[k] for k in self.params.keys()})
        return model
