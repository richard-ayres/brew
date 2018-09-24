from .calculator import Calculator
from .abwcalculator import ABWCalculator
from .gravity_adjuster import adjust_gravity

class ABVCalculator(Calculator):
    required = {'original-gravity', 'final-gravity'}
    defaults = {'temperature': 20, 'calibration-temperature': 20}

    def calculate(self):
        og = adjust_gravity(self['original-gravity'],
                            self['temperature'],
                            self['calibration-temperature'])
        fg = adjust_gravity(self['final-gravity'],
                            self['temperature'],
                            self['calibration-temperature'])
        return 1.3125 * (og - fg)
