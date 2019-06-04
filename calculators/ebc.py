from .calculator import Calculator


class EBC(Calculator):
    required = {'ebc', 'weight'}

    def calculate(self):
        return 0.01 * float(self['weight']) * float(self['ebc'])
