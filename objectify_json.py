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
    return eval("_o{}".format(path))
