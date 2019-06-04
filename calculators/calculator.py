import collections
import abc
import copy

from .exception import CalculatorException


def deref(value):
    return value() if callable(value) else value


def keymap(key):
    return key.replace('_', '-')


class Calculator(collections.abc.MutableMapping):
    """Base class for all calculators"""
    defaults = dict()
    required = set()
    optional = set()

    def __init__(self, *args, **kwargs):
        self.params = dict()

        if args and isinstance(args[0], dict):
            self.update(args[0])

        if 'params' in kwargs:
            self.update(kwargs['params'])
            del kwargs['params']

        if kwargs:
            self.update(kwargs)

    def __getitem__(self, key):
        """FIXME: clean this function up"""
        if isinstance(key, tuple):
            return deref(self.get_params(*key))

        try:
            result = self.params[key]
        except KeyError:
            result = self.defaults[key]

        return deref(result)

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

    def copy(self):
        return copy.deepcopy(self)

    def with_(self, *args, **kwargs):
        """Copy this object with the argument(s) as a property and return new object"""
        obj = self.copy()

        if args and isinstance(args[0], dict):
            obj.update(args[0])

        if 'params' in kwargs:
            obj.update(kwargs['params'])
            del kwargs['params']

        if kwargs:
            obj.update(kwargs)

        return obj

    def update(self, dct):
        dct = {keymap(key): dct[key] for key in dct.keys()}
        keys = dct.keys() & (self.required | self.optional | self.defaults.keys())
        return self.params.update({key:dct[key] for key in keys})

    @abc.abstractmethod
    def calculate(self):
        pass

    def get_params(self, *args):
        result = {}
        args = set(args)

        # Check for any missing parameters
        missing = self.required - self.params.keys() - self.defaults.keys()
        if missing:
            raise CalculatorException('Missing parameters: {:s}'.format(str(missing)))

        result.update({key: self.params[key]
                       for key in (args - result.keys())
                       if key in self.params})

        result.update({key: self.defaults[key]
                       for key in (args - result.keys())
                       if key in self.defaults})

        # make sure we have returned all items requested
        assert len(args - result.keys()) == 0

        return result
