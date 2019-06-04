from .calculator import Calculator


class GravityToPlato(Calculator):
    required = {'specific-gravity'}

    def calculate(self):
        sg = float(self['specific-gravity'])
        return -616.868 + (1111.14 * sg) - (630.272 * sg * sg) + (135.997 * sg*sg*sg)


def gravity_to_plato(sg):
    return GravityToPlato({'specific-gravity': sg}).calculate()
