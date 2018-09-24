from .calculator import Calculator
from .celsius_to_fahrenheit import celsius_to_fahrenheit

# constants
C1 = 1.00130346
C2 = 0.000134722124
C3 = 0.00000204052596 
C4 = 0.00000000232820948

class GravityAdjuster(Calculator):
    required = {'specific-gravity'}
    defaults = {'temperature': 20, 'calibration-temperature': 20}

    def calculate(self):
        sg = float(self['specific-gravity'])
        tr = celsius_to_fahrenheit(self['temperature'])
        tc = celsius_to_fahrenheit(self['calibration-temperature'])

        return sg * ((C1 - C2 * tr + C3 * tr*tr - C4 * tr*tr*tr) / \
                     (C1 - C2 * tc + C3 * tc*tc - C4 * tc*tc*tc))

def adjust_gravity(gravity, temperature, calibration_temperature):
    return GravityAdjuster({'specific-gravity': gravity,
                            'temperature': temperature,
                            'calibration-temperature': calibration_temperature}).calculate()