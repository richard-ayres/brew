from .calculator import Calculator


class HopSchedule(Calculator):
    required = {'hop-additions', 'gravity', 'volume'}

    def __str__(self):
        return "\n".join(map(str, self['hop-additions']))

    def calculate(self):
        return sum(addition.with_(gravity=self['gravity'], volume=self['volume']).calculate()
                   for addition in self['hop-additions'])
