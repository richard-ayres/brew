from .calculator import Calculator

class PlatoToGravity(Calculator):
    required = {'plato'}

    def calculate(self):
        plato = float(self['plato'])
        return 1 + (plato / (258.6 - ((plato/258.2) * 227.1)))

def plato_to_gravity(plato):
    return PlatoToGravity(plato=plato).calculate()
