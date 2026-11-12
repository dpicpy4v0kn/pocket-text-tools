# pocket-text-tools

Small, dependency-free text utilities for everyday development and learning.
Requires Python 3.10 or newer. All processing happens locally.

## Quick start

From a checkout, run without installing anything:

```sh
printf 'Café & Notes!\n' | python3 -m pocket_text_tools slug
# cafe-notes

printf 'hello world\n' | python3 -m pocket_text_tools stats
# {"characters": 12, "words": 2, "lines": 1}

printf 'One\none\nTwo\n' | python3 -m pocket_text_tools unique --ignore-case
# One
# Two
```

Each command accepts an optional UTF-8 file path. Omit it or use `-` to read
standard input. Output is UTF-8; redirect it to a different file to save results:

```sh
python3 -m pocket_text_tools unique notes.txt > cleaned.txt
python3 -m pocket_text_tools stats notes.txt
python3 -m pocket_text_tools --help
```

Do not redirect output to the same file used as input: the shell truncates it
before the program reads it.

To install the `pocket-text-tools` command in a virtual environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install .
pocket-text-tools --help
```

## Behavior

| Command | Behavior |
| --- | --- |
| `stats` | JSON counts of Unicode code points, whitespace-separated words, and logical lines. Empty input has zero lines; a trailing line separator does not add an extra line. |
| `slug` | Lowercase ASCII letters and digits, joined by hyphens. Decomposable accents are removed. Other characters form separators; this is not a transliteration tool. Input with no supported characters produces an empty slug. |
| `unique` | Preserve the first occurrence, spelling and order of each line. Whitespace is significant. Normalize line separators to LF and preserve whether input has a final separator. `--ignore-case` uses Unicode case folding. |

Commands read the complete input into memory and are intended for small text
files. Character counts are code points, not displayed grapheme clusters or
encoded bytes. Files and stdin must use UTF-8. Invalid input or file errors
return status 1; command usage errors return status 2.

## Python API

```python
from pocket_text_tools import count_text, slugify, unique_lines

assert count_text("hello world").words == 2
assert slugify("Café notes") == "cafe-notes"
assert unique_lines("a\nb\na\n") == "a\nb\n"
```

## Development

The test suite uses only the Python standard library:

```sh
python3 -m unittest discover -s tests -v
```

CI runs the same tests on Python 3.10 through 3.14, installs the package and
checks the installed command. No runtime dependencies or credentials are needed.
