from .calculator import Calculator
from .abw_calculator import ABWCalculator


class AccurateABVCalculator(Calculator):
    required = {'original-gravity', 'final-gravity'}
    defaults = {'temperature': 20, 'calibration-temperature': 20}

    def calculate(self):

        abw_calculator = ABWCalculator({
            'final-gravity': self['final-gravity'],
            'original-gravity': self['original-gravity'],
            'temperature': self['temperature'],
            'calibration-temperature': self['calibration-temperature']})

        abw = abw_calculator.calculate()

        return abw * float(self['final-gravity']) / 0.7907

