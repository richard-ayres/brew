from .calculator import Calculator, deref

class HopSchedule(Calculator):
    required = {'hop-additions', 'gravity', 'volume'}

    def __str__(self):
        return "\n".join(map(str, self['hop-additions']))

    def calculate(self):
        total_ibus = 0.0
        for addition in self['hop-additions']:
            addition['gravity'] = self['gravity'] 
            addition['volume'] = self['volume']
            total_ibus += addition.calculate()

        return total_ibus