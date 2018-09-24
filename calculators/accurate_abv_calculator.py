from .abwcalculator import ABWCalculator

class AccurateABVCalculator(ABWCalculator):

    def calculate(self):
        abw = super().calculate()

        return abw * self['final-gravity'] / 0.7907

