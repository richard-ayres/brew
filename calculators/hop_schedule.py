from .calculator import Calculator


class HopSchedule(Calculator):
    required = {'hop-additions', 'gravity', 'volume'}

    def __str__(self):
        return "\n".join(map(str, self['hop-additions']))

    def calculate(self):
        hop_additions = list(self['hop-additions'])
        return sum(addition.with_(gravity=self['gravity'], volume=self['volume']).calculate()
                   for addition in hop_additions)
