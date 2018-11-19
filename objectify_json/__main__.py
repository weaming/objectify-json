import argparse
import sys
import os
import json
import traceback
from . import ObjectifyJSON, get_data_by_path, version
from .obj_json import _unwrap

DEBUG = os.getenv("DEBUG")


def main():
    print_version = len(sys.argv) > 1 and sys.argv[1] in ["-v", "--version"]
    if print_version:
        print(version)
        sys.exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument("expression", default="")
    parser.add_argument(
        "-i", "--input", default="/dev/stdin", help="the file path of input"
    )
    parser.add_argument(
        "-o", "--output", default="/dev/stdout", help="the file path of output"
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=os.getenv("JSON_INDENT"),
        help="the indent of json output",
    )
    parser.add_argument(
        "--safe",
        default=False,
        action="store_true",
        help="dump json without default parameter",
    )
    parser.add_argument(
        "--transparent",
        default=False,
        action="store_true",
        help="this program will do nothing to the data",
    )
    parser.add_argument(
        "--wrapped",
        default=False,
        action="store_true",
        help="print the result ObjectifyJSON",
    )
    args = parser.parse_args()

    try:
        with open(args.input) as f:
            data = json.loads(f.read())
    except Exception as e:
        print(f"IO error: {e}")
        sys.exit(1)

    if not args.transparent:
        try:
            obj = get_data_by_path(data, args.expression, retry=True, unwrap=False)
        except Exception as e:
            if DEBUG:
                print(data)
                traceback.print_exc()
            else:
                print(e)
            sys.exit(1)

    try:
        with open(args.output, "w") as out:
            if args.wrapped:
                out.write(repr(obj))
            else:
                out.write(
                    json.dumps(
                        obj._data,
                        ensure_ascii=False,
                        indent=args.indent,
                        default=None if args.safe else _unwrap,
                    )
                )
    except Exception as e:
        print(data)
        print(f"IOError: {e}")
