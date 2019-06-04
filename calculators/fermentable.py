from .calculator import Calculator
from .ebc import EBC as EBCCalculator

from collections import namedtuple


Result = namedtuple('Result', ['extract', 'ebc'])


class Fermentable(Calculator):
    required = {'name', 'extract-max',
                'weight', 'ebc'}
    optional = {'fermentability'}
    defaults = {'is-extract': False}

    def __init__(self, name, extract_max, fermentability, ebc, *args, **kwargs):
        kwargs['name'] = name
        kwargs['extract-max'] = extract_max
        kwargs['fermentability'] = fermentability
        kwargs['ebc'] = ebc
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "{:s} [{:.0f} grams]".format(self['name'], self['weight'])

    def __repr__(self):
        return str(self)

    def calculate(self):
        ebc = EBCCalculator(ebc=self['ebc'], weight=self['weight']).calculate()
        extract = self['weight'] * self['extract-max'] / 1000

        return Result(extract, ebc)


class Extract(Fermentable):
    def calculate(self):
        self['efficiency'] = 100.0
        return super().calculate()

