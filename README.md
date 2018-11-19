# Objectify JSON

Make accessing JSON like data more convenient.

## Features

* Access dict value via dot `.` (`data.a.b.c`).
* Always return `ObjectifyJSON` type, which holds the data with type of dict, list or any other primitive types.
* Use `x._data` to get the real data.
* Always return `ObjectifyJSON(None)` if doesn't exist.
* An CLI tool named `object` to process JSON data.

## Install

```
pip3 install objectify-json
```

## Example

See `test.py`

## Functions to process data in batch

* The return value is always `ObjectifyJOSN` too!
* The return value of lambda funtions will always be unwrapped to primitive types.
* Most of the `fn_*` functions accept optional `unwrap` parameter to enable passing the underlying value as primitive types to lambda. Default is False.

### Common

Following methods of `ObjectifyJOSN` accept optional `unwrap` to unwrap `ObjectifyJOSN` data to the underlying built-in data, the default value is `False`.

* `fn_map(fn, unwrap=False)`: `map` on the iterator
* `fn_reduce(fn, initializer=None, unwrap=False)`: `reduce` on the iterator, lambda as the first positional parameter, optional `initializer` parameter will be passed to built-in `reduce`.
* `fn_lambda(fn, unwrap=False)`: value in-and-out
* `fn_filter(fn, unwrap=False)`: `filter` on the iterator

### Dict

* `fn_keys()`: Return keys as list.
* `fn_values()`: Return values as list.
* `fn_items()`: Return items as list. Element has the type `tuple`, e.g. `("key", "value")`.
* `fn_include_keys(keys)`: Filter dict. Keep the `keys` you give.
* `fn_exclude_keys(keys)`: Filter dict. Remove the `keys` you give.
* `fn_filter_by_value(fn)`: Filter dict. Filter by the lambda you give, which accept the value of dict item.
* `fn_filter_by_kv(fn)`: Filter dict. Filter by the lambda you give, which accept `key` and `value` two variables.
* `fn_update(key, fn, unwrap=False)`: Update dict value. The lambda you give accept the origin value and return a new value.
* `fn_items_update(fn, unwrap=False)`: Update dict value. The lambda you give accept `key` and `value` two variables and return a new value.
* `fn_rename(mapping)`: Update dict key. The `mapping` is a list of two-elements list.

### List

* `fn_sort(fn)`: Sort the list in place. The lambda you give will be passed as `key` argument to the `sort` method of list.
* `fn_dedup(fn=None, all=True)`: Dedup the elements in list. If `all` if `False`, the duplication will checked by comparing current value between last value, else will compare to all appeared before.
