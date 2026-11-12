"""Command-line interface; input and output use UTF-8."""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from . import count_text, slugify, unique_lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("stats", "Count characters, words and lines as JSON"),
        ("slug", "Create an ASCII URL slug"),
        ("unique", "Remove duplicate lines in input order"),
    ):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("file", nargs="?", default="-", help="UTF-8 file (default: stdin)")
        if name == "unique":
            command.add_argument("--ignore-case", action="store_true")
    args = parser.parse_args()
    try:
        text = (sys.stdin.buffer.read().decode("utf-8") if args.file == "-"
                else Path(args.file).read_bytes().decode("utf-8"))
        if args.command == "stats":
            output = json.dumps(asdict(count_text(text))) + "\n"
        elif args.command == "slug":
            output = slugify(text) + "\n"
        else:
            output = unique_lines(text, ignore_case=args.ignore_case)
        sys.stdout.buffer.write(output.encode("utf-8"))
        return 0
    except (OSError, UnicodeError) as error:
        print(f"pocket-text-tools: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
