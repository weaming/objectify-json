from functools import reduce
from .pure_eval import eval_with_context

LIST = "LIST"
DICT = "DICT"
BASIC = "BASIC"


class ObjectifyJSON:
    def __init__(self, data):
        """
        Wrapper on dict and list. You can access dict value by dot,
        e.g. self.a.b[3].c
        """
        self._data = data
        self._init()

    @property
    def type(self):
        if isinstance(self._data, (list, tuple)):
            return LIST
        elif isinstance(self._data, dict):
            return DICT
        elif isinstance(self._data, (int, float, str)) or self._data is None:
            return BASIC

    def __getattr__(self, item):
        if self.type == DICT:
            if item in self._data:
                return ObjectifyJSON(self._data[item])

            if item == "fn_keys":
                return lambda: ObjectifyJSON(list(self._data.keys()))
            elif item == "fn_values":
                return lambda: ObjectifyJSON(list(self._data.values()))
            elif item == "fn_items":
                return lambda: ObjectifyJSON(list(self._data.items()))

        if item == "fn_map":

            def fn_map(fn, unwrap=True):
                return ObjectifyJSON(list(map(fn, self._data if unwrap else self)))

            return fn_map

        elif item == "fn_reduce":

            def fn_reduce(fn, initializer=None, unwrap=True):
                if initializer is None:
                    return ObjectifyJSON(reduce(fn, self._data if unwrap else self))
                else:
                    return ObjectifyJSON(reduce(fn, self._data, initializer))

            return fn_reduce

        elif item == "fn_lambda":

            def fn_lambda(fn, unwrap=True):
                return ObjectifyJSON(fn(self._data if unwrap else self))

            return fn_lambda

        elif item == "fn_filter":

            def fn_filter(fn, unwrap=True):
                return ObjectifyJSON(list(filter(fn, self._data if unwrap else self)))

            return fn_filter

        # get the magic methods on data
        if item.startswith("__") and item.endswith("__"):
            return getattr(self._data, item)

        return ObjectifyJSON(None)

    def __getitem__(self, key):
        if self.type == DICT:
            if key in self._data:
                return ObjectifyJSON(self._data[key])
        elif self.type == LIST:
            try:
                return ObjectifyJSON(self._data[key])
            except IndexError:
                pass
        return ObjectifyJSON(None)

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, repr(self._data))

    def __str__(self):
        return str(self._data)

    def __iter__(self):
        """ iter on the real data """
        iterator = self._data.__iter__()
        real_next = iterator.__next__

        rv = real_next()
        while rv:
            yield ObjectifyJSON(rv)
            rv = real_next()

    def __bool__(self):
        return bool(self._data)

    def _init(self):
        if self.type == DICT:

            def items():
                for k, v in self._data.items():
                    yield ObjectifyJSON(k), ObjectifyJSON(v)

            self.items = items


def get_data_by_path(data, path):
    if isinstance(data, ObjectifyJSON):
        o = data
    else:
        o = ObjectifyJSON(data)
    return eval_with_context("o{}".format(path), context={"o": o})._data
