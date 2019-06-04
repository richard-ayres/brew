from .calculator import Calculator
from .gravity_to_plato import gravity_to_plato
from .gravity_adjuster import adjust_gravity


class ABWCalculator(Calculator):
    optional = {'temperature',
                'original-extract', 'real-extract',
                'original-gravity', 'final-gravity'}
    defaults = {'temperature': 20, 'calibration-temperature': 20}

    def calculate(self):
        if 'original-extract' not in self:
            self['original-extract'] = gravity_to_plato(adjust_gravity(self['original-gravity'],
                                                                       self['temperature'],
                                                                       self['calibration-temperature']))

        if 'real-extract' not in self:
            if 'apparent-extract' not in self:
                self['apparent-extract'] = gravity_to_plato(adjust_gravity(self['final-gravity'],
                                                                       self['temperature'],
                                                                       self['calibration-temperature']))

            self['real-extract'] = (0.1948 * self['original-extract']) + \
                                   (0.8052 * self['apparent-extract'])

        return 0.01 * (self['original-extract'] - self['real-extract']) / \
                      (2.0665 - (0.010665 * self['original-extract']))