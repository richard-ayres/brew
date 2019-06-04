from .calculator import Calculator


class FahrenheitToCelsius(Calculator):
    required = {'temperature'}

    def calculate(self):
        return 5.0 * (float(self['temperature']) - 32.0) / 9.0;


def fahrenheit_to_celsius(temperature):
    return FahrenheitToCelsius(temperature=temperature).calculate()