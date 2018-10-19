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

    @property
    def type(self):
        if isinstance(self._data, (list, tuple)):
            return LIST
        elif isinstance(self._data, dict):
            return DICT
        elif isinstance(self._data, (int, float, str)) or self._data is None:
            return BASIC

    def __getattr__(self, item):
        if self.type == DICT and item in self._data:
            if item in self._data:
                return ObjectifyJSON(self._data[item])

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


def get_data_by_path(data, path):
    _o = ObjectifyJSON(data)
    return eval("_o{}".format(path))._data


class Formatter:
    context = ObjectifyJSON(None)

    def format_value(self, value: str):
        return value.format(self=self.context)

    def parse_dict(self, data: dict):
        for k, v in data.copy().items():
            if isinstance(v, dict):
                v = self.parse_dict(v)
            elif isinstance(v, list):
                v = self.parse_list(v)
            elif isinstance(v, (int, float, bool)):
                v = v
            elif isinstance(v, str):
                v = self.format_value(v)

            data[self.format_value(k)] = v
        return data

    def parse_list(self, data: list):
        for i, v in enumerate(data.copy()):
            if isinstance(v, dict):
                v = self.parse_dict(v)
            elif isinstance(v, list):
                v = self.parse_list(v)
            elif isinstance(v, (int, float, bool)):
                v = v
            elif isinstance(v, str):
                v = self.format_value(v)

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
