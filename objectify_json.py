import sys
import argparse
import json
from functools import reduce

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
        _o = data
    else:
        _o = ObjectifyJSON(data)
    return eval("_o{}".format(path))._data


class Formatter:
    context = ObjectifyJSON(None)

    def format_value(self, value):
        if isinstance(value, str):
            try:
                return value.format(self=self.context)
            except KeyError:
                print(value)
                print(self.context)
                raise
        return value

    def parse_dict(self, data: dict):
        for k, v in data.copy().items():
            if isinstance(v, dict):
                v = self.parse_dict(v)
            elif isinstance(v, list):
                v = self.parse_list(v)
            elif isinstance(v, str):
                v = self.format_value(v)
            else:
                v = v

            data[self.format_value(k)] = v
        return data

    def parse_list(self, data: list):
        for i, v in enumerate(data.copy()):
            if isinstance(v, dict):
                v = self.parse_dict(v)
            elif isinstance(v, list):
                v = self.parse_list(v)
            elif isinstance(v, str):
                v = self.format_value(v)
            else:
                v = v

            data[i] = v
        return data

    def parse_cofig(self, data):
        # get the real data
        if isinstance(data, ObjectifyJSON):
            data = data._data

        if isinstance(data, (list, tuple)):
            return self.parse_list(data)
        if isinstance(data, dict):
            return self.parse_dict(data)
        if isinstance(data, str):
            return self.format_value(data)
        raise NotImplementedError(str(type(data)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("expression", default="")
    parser.add_argument(
        "-i", "--input", default="/dev/stdin", help="the file path of input"
    )
    parser.add_argument(
        "-o", "--output", default="/dev/stdout", help="the file path of output"
    )
    parser.add_argument("--indent", type=int, help="the indent of json output")
    args = parser.parse_args()

    try:
        with open(args.input) as f:
            data = json.loads(f.read())
    except Exception as e:
        print(f"IO error: {e}")
        sys.exit(1)

    try:
        result = get_data_by_path(data, args.expression)
    except Exception as e:
        print(e)
        sys.exit(1)

    with open(args.output, "w") as out:
        out.write(json.dumps(result, ensure_ascii=False, indent=args.indent))
