# Objectify JSON

Make accessing JSON like data more convenient.

## Features

* Access dict value via dot `.` (`data.a.b.c`).
* Always return `ObjectifyJSON` type, which holds the data having type dict, list or any other primitive types.
* Use `x._data` to get the real data.
* Always return `ObjectifyJSON(None)` if doesn't exist.
* Iterate on dict or list via `for` loop. The iteration elements' type are `ObjectifyJSON` too!
* Iterate on dict via `.fn_keys()`, `.fn_values()` or `.fn_items()`.
* Process data in a collection via `.fn_map()`, `.fn_reduce()` or `.fn_filter()`.
* An CLI tool named `object` to process JSON data.

## Install

```
pip3 install objectify-json
```

## Example

See `test.py`
