from functools import reduce
from threading import Lock
from .pure_eval import eval_with_context
import itertools

LIST = "LIST"
DICT = "DICT"
BASIC = "BASIC"

STATE_LOCK = Lock()
GLOBAL_STATE = {}


def update_global_state(k, v):
    with STATE_LOCK:
        GLOBAL_STATE[k] = v


class ObjectifyJSON:
    def __init__(self, data, path=None):
        """
        Wrapper on dict and list. You can access dict value by dot,
        e.g. self.a.b[3].c
        """
        self._data = data
        self._path = path or []

    @property
    def __type(self):
        if isinstance(self._data, (list, tuple)):
            return LIST
        if isinstance(self._data, dict):
            return DICT
        if isinstance(self._data, (int, float, str)) or self._data is None:
            return BASIC

    def __getattr__(self, item):
        if self.__type == DICT:
            if item in self._data:
                rv = ObjectifyJSON(self._data[item])
                return self._inherit_meta(rv, item)
        elif self.__type == LIST:
            if item.startswith("i") and item[1:].isdigit():
                return self[int(item[1:])]

        # get methods
        fn = self.__get_fn(item)
        if fn:
            return fn

        # get the magic methods on data
        if item.startswith("__") and item.endswith("__"):
            return getattr(self._data, item)

        # return default
        rv = ObjectifyJSON(None)
        return self._inherit_meta(rv, item)

    def __get_fn(self, item):
        """
        :return: function or None
        """
        if self.__type == DICT:
            if item == "fn_keys":
                return lambda: ObjectifyJSON(list(self._data.keys()))
            elif item == "fn_values":
                return lambda: ObjectifyJSON(list(self._data.values()))
            elif item == "fn_items":
                return lambda: ObjectifyJSON(list(self._data.items()))

            # other special methods
            elif item == "fn_include_keys":
                return lambda keys: ObjectifyJSON(
                    {k: v for k, v in self._data.items() if k in keys}
                )
            elif item == "fn_exclude_keys":
                return lambda keys: ObjectifyJSON(
                    {k: v for k, v in self._data.items() if k not in keys}
                )
            elif item == "fn_filter_by_value":
                return lambda fn: ObjectifyJSON(
                    {k: v for k, v in self._data.items() if fn(v)}
                )
            elif item == "fn_filter_by_kv":
                return lambda fn: ObjectifyJSON(
                    {k: v for k, v in self._data.items() if fn(k, v)}
                )
            elif item == "fn_update":

                def fn_update(key, fn, unwrap=False):
                    new = fn(self._data[key] if unwrap else getattr(self, key))
                    self._data[key] = _unwrap(new)
                    return self

                return fn_update
            elif item == "fn_items_update":

                def fn_items_update(fn, unwrap=False):
                    for k, v in self._data.items():
                        v = v if unwrap else ObjectifyJSON(v)
                        self._data[k] = _unwrap(fn(k, v))
                    return self

                return fn_items_update

            elif item == "fn_rename":

                def fn_rename(mapping):
                    for k, k1 in mapping:
                        if k in self._data:
                            self._data[k1] = self._data.pop(k)
                    return self

                return fn_rename

        if self.__type == LIST:
            if item == "fn_sort":

                def fn_sort(fn):
                    self._data.sort(key=fn)
                    return self

                return fn_sort

            elif item == "fn_dedup":

                def fn_dedup(fn=None, all=True):
                    if not fn:
                        fn = lambda x: x

                    new = []
                    keys = []
                    for x in self._data:
                        key = fn(x)
                        if all:
                            if_v = key not in keys
                        else:
                            if_v = not keys or key != keys[-1]

                        if if_v:
                            new.append(x)
                            keys.append(key)

                    self._data = new
                    return self

                return fn_dedup

            elif item == "fn_chain":

                def fn_chain(unwrap=False):
                    flat = list(
                        itertools.chain(*(x._data if unwrap else x for x in self))
                    )
                    new_data = ObjectifyJSON(flat)
                    return _wrap(_unwrap(new_data))

                return fn_chain

            elif item == "fn_intersection":

                def fn_intersection(unwrap=False):
                    intersection = None
                    for x in self:
                        x = [_unwrap(xx) for xx in x]
                        if intersection is None:
                            intersection = set(x)
                        else:
                            intersection = intersection & set(x)
                    new_data = ObjectifyJSON(list(intersection))
                    return _wrap(_unwrap(new_data))

                return fn_intersection

        if item == "fn_map":

            def fn_map(fn, unwrap=False):
                rv = map(fn, self._data if unwrap else self)
                rv = [_unwrap(x) for x in rv]
                return ObjectifyJSON(rv)

            return fn_map

        elif item == "fn_reduce":

            def fn_reduce(fn, initializer=None, unwrap=False):
                data = self._data if unwrap else self
                if initializer is None:
                    return ObjectifyJSON(_unwrap(reduce(fn, data)))
                else:
                    return ObjectifyJSON(_unwrap(reduce(fn, data, initializer)))

            return fn_reduce

        elif item == "fn_lambda":

            def fn_lambda(fn, unwrap=False):
                rv = fn(self._data if unwrap else self)
                return ObjectifyJSON(_unwrap(rv))

            return fn_lambda

        elif item == "fn_filter":

            def fn_filter(fn=None, unwrap=False):
                rv = filter(fn, self._data if unwrap else self)
                rv = [_unwrap(x) for x in rv]
                return ObjectifyJSON(rv)

            return fn_filter

        else:
            if not GLOBAL_STATE.get("retry") or item.startswith("fn_"):
                return None

            # try to add `fn_` prefix
            return self.__get_fn(f"fn_{item}")

    def __getitem__(self, key):
        if self.__type == DICT:
            if key in self._data:
                rv = ObjectifyJSON(self._data[key])
                return self._inherit_meta(rv, key)
        elif self.__type == LIST:
            try:
                rv = ObjectifyJSON(self._data[key])
                return self._inherit_meta(rv, key)
            except IndexError:
                pass

        rv = ObjectifyJSON(None)
        return self._inherit_meta(rv, key)

    def _inherit_meta(self, new, key):
        new._path = self._path + [key]
        return new

    def __repr__(self):
        return "<{}: ({}) {}>".format(
            self.__class__.__name__, self._path, repr(self._data)
        )

    def __str__(self):
        return str(self._data)

    def __iter__(self):
        """ iter on the real data """
        if self._data is None:
            return ObjectifyJSON(None)

        iterator = self._data.__iter__()
        real_next = iterator.__next__

        rv = real_next()
        while 1:
            yield ObjectifyJSON(rv)
            try:
                rv = real_next()
            except StopIteration:
                return

    def __bool__(self):
        return bool(self._data)

    def __call__(self, *args, **kwargs):
        raise Exception(f"{repr(self)} is not callable: args {args}, kwargs {kwargs}")


def get_data_by_path(data, path, retry=False, unwrap=True):
    if isinstance(data, ObjectifyJSON):
        o = data
    else:
        o = ObjectifyJSON(data)

    update_global_state("retry", retry)
    rv = eval_with_context("o{}".format(path), context={"o": o})
    if unwrap:
        return rv._data
    return rv


def _unwrap(data):
    if isinstance(data, ObjectifyJSON):
        data = data._data

    if isinstance(data, list):
        return [_unwrap(x) for x in data]
    if isinstance(data, tuple):
        return tuple(_unwrap(x) for x in data)
    if isinstance(data, dict):
        return {_unwrap(k): _unwrap(v) for k, v in data.items()}
    return data


def _wrap(data):
    return ObjectifyJSON(_unwrap(data))
