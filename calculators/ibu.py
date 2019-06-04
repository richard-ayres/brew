import logging

from .calculator import Calculator
from .utilization import Utilization


class IBU(Calculator):
    required = {'utilization', 'alpha', 'weight', 'volume'}

    def calculate(self):
        utilization = float(self['utilization'])
        alpha = float(self['alpha'])
        weight = float(self['weight'])
        volume = float(self['volume'])

        ibu = 1000.0 * utilization * alpha * weight / volume

        logging.debug(
            """IBU Calculator:
    Utilization={utilization:.2f}
    Alpha={alpha}
    Weight={weight}
    Volume={volume}
    IBU={ibu:.1f}""".format(
                utilization=utilization,
                alpha=alpha,
                weight=weight,
                volume=volume,
                ibu=ibu))

        return ibu


def calculate_ibu(gravity, boil_time, alpha, weight, volume):
    return IBU(utilization=Utilization({'gravity': gravity,
                                        'boil-time': boil_time}),
               alpha=alpha,
               weight=weight,
               volume=volume).calculate()

