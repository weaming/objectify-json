# Objectify JSON

Make accessing JSON like data more convenient.

## Features

* Access dict value via dot `.` (`data.a.b.c`).
* Always return `ObjectifyJSON` type, which holds the data with type of dict, list or any other primitive types.
* Use `x._data` to get the real data.
* Always return `ObjectifyJSON(None)` if doesn't exist.
* Batch process data
    * Process data in a collection via `.fn_map()`, `.fn_reduce()` or `.fn_filter()`.
    * Iterate on dict or list via `for` loop. The iteration elements' type are `ObjectifyJSON` too!
    * Iterate on dict via `.fn_keys()`, `.fn_values()`, `.fn_items()`, or `fn_items_update()`.
    * Sort list inplace via `fn_sort`.
    * The return values of lambda funtion will always be unwrapped to primitive types.
    * The `fn_*` functions all accept `unwrap` keyword flag to enable passing the primitive types to lambda. Default is False.
* An CLI tool named `object` to process JSON data.

## Install

```
pip3 install objectify-json
```

## Example

See `test.py`

## Functions
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

* `fn_sort`: sort the list, the lambda you give is passed as `key` argument to the `sort` method of list
