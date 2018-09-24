"""Utilization calculator derived from Tinseth at http://www.realbeer.com/hops/research.html"""
import math
import calculators

class Utilization(calculators.Calculator):
    required = {'gravity', 'boil-time'}

    def calculate(self):
        gravity = float(self['gravity']) / 1000.0
        boil_time = float(self['boil-time'])

        bigness = 1.65 * math.pow(0.000125, (gravity-1.0))
        boiltime_factor = (1 - math.exp(-0.04 * boil_time)) / 4.15

        utilization = bigness * boiltime_factor

        return utilization

def utilization(gravity, boil_time):
    return Utilization({'gravity': gravity, 'boil-time': boil_time}).calculate()

