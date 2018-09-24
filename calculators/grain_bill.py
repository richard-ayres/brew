"""The grain bill, incorporating malt extracts and sugars"""
from functools import reduce

from .calculator import Calculator, deref


class GrainBill(Calculator):
    required = {'fermentables', 'efficiency', 'volume'}

    def __str__(self):
        return "\n".join(map(str, self['fermentables']))

    def calculate(self):
        """Calculate expected original gravity, and expected EBC"""

        total_gravity = 0.0
        for fermentable in self['fermentables']:
            total_gravity += fermentable()[0] if fermentable['is-extract'] else \
                             fermentable()[0] * self['efficiency']

        total_gravity = 1000.0 + total_gravity / self['volume']

        total_ebc = sum(fermentable()[1] for fermentable in self['fermentables']) / self['volume']

        return (total_gravity, total_ebc)




