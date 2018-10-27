import argparse
import sys
import os
import json
import traceback
from . import ObjectifyJSON, get_data_by_path
from .obj_json import _unwrap

DEBUG = os.getenv("DEBUG")


def main():
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
    args = parser.parse_args()

    try:
        with open(args.input) as f:
            data = json.loads(f.read())
    except Exception as e:
        print(f"IO error: {e}")
        sys.exit(1)

    try:
        result = get_data_by_path(data, args.expression)
    except Exception as e:
        if DEBUG:
            traceback.print_exc()
        else:
            print(e)
        sys.exit(1)

    try:
        with open(args.output, "w") as out:
            out.write(
                json.dumps(
                    result,
                    ensure_ascii=False,
                    indent=args.indent,
                    default=None if args.safe else _unwrap,
                )
            )
    except Exception as e:
        print(result)
        print(f"IOError: {e}")
