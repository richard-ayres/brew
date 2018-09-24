from .calculator import Calculator
from .utilization import Utilization

class IBU(Calculator):
    required = {'utilization', 'alpha', 'weight', 'volume'}

    def calculate(self):
        utilization = float(self['utilization'])
        alpha = float(self['alpha'])
        weight = float(self['weight'])
        volume = float(self['volume'])

        return 1000 * utilization * alpha * weight / volume

def calculate_IBUs(gravity, boil_time, alpha, weight, volume):
    return IBU(utilization=Utilization({'gravity': gravity,
                                        'boil-time': boil_time}),
               alpha=alpha,
               weight=weight,
               volume=volume).calculate()

