from .calculator import Calculator
from .ibu import calculate_IBUs

class HopAddition(Calculator):
    required = {'name', 'alpha', 'weight', 'boil-time', 'gravity', 'volume'}

    def __init__(self, name, *args, **kwargs):
        kwargs['name'] = name
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "{:s} {:.1f}%  [{:.1f} grams]".format(self['name'], self['alpha'], self['weight'])

    def calculate(self):
        return calculate_IBUs(self['gravity'],
                              self['boil-time'],
                              self['alpha'] / 100,
                              self['weight'],
                              self['volume'])