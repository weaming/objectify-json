from .obj_json import ObjectifyJSON


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
