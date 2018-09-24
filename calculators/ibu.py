from .calculator import Calculator
from .utilization_tinseth import TinsethUtilization

class IBU(Calculator):
    required = {'utilization', 'alpha', 'weight', 'volume'}

    def calculate(self):
        utilization = float(self['utilization'])
        alpha = float(self['alpha'])
        weight = float(self['weight'])
        volume = float(self['volume'])

        return 1000 * utilization * alpha * weight / volume

def calculate_IBUs(gravity, boil_time, alpha, weight, volume,
                   utilization_calculator=TinsethUtilization):
    return IBUCalculator(utilization=utilization_calculator({'gravity': gravity,
                                                             'boil-time': boil_time}),
                         alpha=alpha,
                         weight=weight,
                         volume=volume).calculate()

