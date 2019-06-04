"""Utilization calculator derived from Tinseth at http://www.realbeer.com/hops/research.html"""
import logging
import math

from calculators import Calculator


class Utilization(Calculator):
    required = {'gravity', 'boil-time'}

    def calculate(self):
        gravity = float(self['gravity'])
        boil_time = float(self['boil-time'])

        bigness = 1.65 * math.pow(0.000125, (gravity-1.0))
        boiltime_factor = (1 - math.exp(-0.04 * boil_time)) / 4.15

        utilization = bigness * boiltime_factor

        logging.debug(
            """Utilization Calculator:
    Gravity={gravity:.3f}
    Boil time={boil_time}
    Bigness={bigness:.2f}
    Boiltime Factor={boiltime_factor:.3f}
    Utilization={utilization:.3f}""".format(
                gravity=gravity,
                boil_time=boil_time,
                bigness=bigness,
                boiltime_factor=boiltime_factor,
                utilization=utilization))

        return utilization


def utilization(gravity, boil_time):
    return Utilization({'gravity': gravity, 'boil-time': boil_time}).calculate()

