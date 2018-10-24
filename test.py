from objectify_json import ObjectifyJSON, get_data_by_path

data = {
    "login": {"password": "password", "username": "admin"},
    "data": [
        {
            "id": "it's an id",
            "request": {"headers": None, "method": "get", "query": {"a": 3, "b": 4}},
        },
        {"id": "id2", "request": {"method": "post", "query": {"a": 3, "b": 4}}},
    ],
}

o = ObjectifyJSON(data)

print(o.login.username)
print(o.data[0].id)
_len = o.data[0].id.len
print(_len, bool(_len))
print(o.data[0].request.query.a)
print(o.data[1].id)

print(get_data_by_path(data, ".data[0].id"))

print("-----")
for x in o:
    print(repr(x))

print("-----")
print(o.data.first)
print(o.data.last)
print(o.data.last.keys())
print(o.data.last.values())
