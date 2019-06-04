from .calculator import Calculator


class CelsiusToFahrenheit(Calculator):
    required = {'temperature'}

    def calculate(self):
        return float(self['temperature']) * 9.0 / 5.0 + 32.0


def celsius_to_fahrenheit(temperature):
    return CelsiusToFahrenheit(temperature=temperature).calculate()