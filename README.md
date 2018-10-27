# Objectify JSON

Make accessing JSON like data more convenient.

## Features

* Access dict value via dot `.` (`data.a.b.c`).
* Always return `ObjectifyJSON` type, which holds the data having type dict, list or any other primitive types.
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
