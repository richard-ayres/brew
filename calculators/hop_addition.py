from .calculator import Calculator
from .ibu import calculate_ibu


class HopAddition(Calculator):
    required = {'name', 'alpha', 'weight', 'boil-time', 'gravity', 'volume'}

    def __init__(self, name, *args, **kwargs):
        kwargs['name'] = name
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "{name} {alpha:.1f}%  [{weight:.1f} grams]".format(
            name=self['name'], alpha=self['alpha'], weight=self['weight'])

    def calculate(self):
        return calculate_ibu(self['gravity'],
                             self['boil-time'],
                             self['alpha'] / 100,
                             self['weight'],
                             self['volume'])