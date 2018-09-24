import collections
import abc

from .exception import CalculatorException

def deref(value):
    return value() if callable(value) else value

class Calculator(collections.abc.MutableMapping):
    defaults = dict()
    required = set()
    optional = set()

    def __init__(self, *args, **kwargs):
        self.params = dict()

        if args and isinstance(args[0], dict):
            self.params.update(args[0])

        if 'params' in kwargs:
            self.params.update(kwargs['params'])
            del kwargs['params']

        if kwargs:
            self.params.update(kwargs)

    def __getitem__(self, key):
        """FIXME: clean this function up"""
        result = None

        if isinstance(key, tuple):
            result = self.get_params(*key)

        else:
            if key not in self.params and key not in self.defaults:
                raise KeyError("Key '{:s}' not present".format(str(key)))

            result = self.params[key] if key in self.params else self.defaults[key]

        if isinstance(result, tuple):
            result = tuple(map(deref, result))

        elif isinstance(result, list):
            result = list(map(deref, result))

        elif isinstance(result, dict):
            result = {key:deref(result[key]) for key in result}

        else:
            result = deref(result)

        return result

    def __setitem__(self, key, value):
        self.params[key] = value

    def __delitem__(self, key):
        del self.params[key]

    def __iter__(self):
        return iter(self.params)

    def __len__(self):
        return len(self.params)

    def __call__(self):
        return self.calculate()

    @abc.abstractmethod
    def calculate(self):
        pass

    def get_params(self, *args):
        result = {}

        # Check for any missing parameters
        missing = self.required - self.params.keys() - self.defaults.keys()
        if missing:
            raise CalculatorException('Missing parameters: {:s}'.format(str(missing)))

        result.update({key:self.params[key] for key in (args - result.keys())
                                             if key in self.params})
        result.update({key:self.defaults[key] for key in (args - result.keys())
                                               if key in self.defaults})

        return result