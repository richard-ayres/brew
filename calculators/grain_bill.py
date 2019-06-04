"""The grain bill, incorporating malt extracts and sugars"""
from collections import namedtuple

from .calculator import Calculator


Result = namedtuple('Result', ['gravity', 'ebc'])


class GrainBill(Calculator):
    required = {'fermentables', 'efficiency', 'volume'}

    def __str__(self):
        return "\n".join(map(str, self['fermentables']))

    def calculate(self):
        """Calculate expected original gravity, and expected EBC"""

        total_gravity = sum(fermentable().extract * (1.0 if fermentable['is-extract'] else self['efficiency'])
                            for fermentable in self['fermentables'])
        total_gravity = (1000.0 + total_gravity / self['volume']) / 1000.0

        total_ebc = sum(fermentable().ebc for fermentable in self['fermentables']) / self['volume']

        return Result(total_gravity, total_ebc)

