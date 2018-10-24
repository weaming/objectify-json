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

# existed properties
print(o.login.username)
print(o.data[0].id)
print(o.data[0].request.query.a)

print("-----")
v = o.data[0].id.some_property  # non-exist property
print(v, bool(v))

print("-----")
print(get_data_by_path(data, ".data[0].id"))  # get data by path

print("-----")
for x in o:
    print(repr(x))  # repr

print("-----")
print(o.data[0].fn_keys())  # keys
print(o.data[0].fn_values())  # values

print("-----")
print(o.data[0].fn_map(lambda x: str(x)))  # map
print(o.data[0].fn_reduce(lambda a, b: a + b))  # reduce

print(o.data[0].fn_lambda(lambda x: len(str(x))))  # lambda
