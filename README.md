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
* The `fn_*` functions all accept optional `unwrap` parameter to enable passing the underlying value as primitive types to lambda. Default is False.

### Common

Following methods of `ObjectifyJOSN` accept optional `unwrap` to unwrap `ObjectifyJOSN` data to the underlying built-in data, the default value is `False`.

* `fn_map`: `map` on the iterator
* `fn_reduce`: `reduce` on the iterator, lambda as the first positional parameter, optional `initializer` parameter will be passed to built-in `reduce`.
* `fn_lambda`: value in-and-out
* `fn_filter`: `filter` on the iterator

### Dict

* `fn_keys`: return keys as list
* `fn_values`: return values as list
* `fn_items`: return items as list, element has the type `tuple`, e.g. `("key", "value")`
* `fn_include_keys`: filter dict, keep the `keys` you give
* `fn_exclude_keys`: filter dict, remove the `keys` you give
* `fn_filter_by_value`: filter dict, filter by the lambda you give, which accept the value of dict item
* `fn_filter_by_kv`: filter dict, filter by the lambda you give, which accept `key` and `value` two variables
* `fn_update`: update dict value, the lambda you give accept the origin value and return a new value
* `fn_items_update`: update dict value, the lambda you give accept `key` and `value` two variables


### List

* `fn_sort`: sort the list in place, the lambda you give will be passed as `key` argument to the `sort` method of list
