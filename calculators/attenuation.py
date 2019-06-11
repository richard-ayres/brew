import logging

from .calculator import Calculator
from .grain_bill import GrainBill


class Attenuation(Calculator):
    defaults = {'yeast-efficiency': 0.75, 'brew-efficiency': 0.75}
    required = {'fermentables', 'volume'}
    optional = {'original-gravity'}

    def calculate(self):

        try:
            og = self['original-gravity']
        except KeyError:
            gb = GrainBill(efficiency=self['brew-efficiency'],
                           volume=self['volume'],
                           fermentables=self['fermentables'])
            og = gb.calculate().gravity

        fermentables = list(self['fermentables'])

        yeast_efficiency_factor = 100 * self['yeast-efficiency'] / 62.0

        total_extract = sum(fermentable().extract * fermentable['fermentability'] * (self['brew-efficiency'] if not fermentable['is-extract'] else 1.0)
                            for fermentable in fermentables)

        total_extract = total_extract / self['volume']

        final_gravity = (1000 * og - yeast_efficiency_factor * total_extract)/1000.0

        logging.debug("""Attenuation:
    Yeast efficiency factor={yef:.3f}
    Total fermentables={total:.2f}
    OG={og:.3f}
    FG={fg:.3f}""".format(
            yef=yeast_efficiency_factor,
            total=total_extract,
            og=og,
            fg=final_gravity
        ))

        self['final-gravity'] = final_gravity

        return final_gravity
