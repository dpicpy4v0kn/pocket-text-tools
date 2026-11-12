"""Small, predictable text transformations."""

import re
import unicodedata
from dataclasses import dataclass


@dataclass(frozen=True)
class TextStats:
    characters: int
    words: int
    lines: int


def count_text(text: str) -> TextStats:
    """Count Unicode code points, whitespace-separated words and logical lines."""
    return TextStats(len(text), len(text.split()), len(text.splitlines()))


def slugify(text: str) -> str:
    """Make a lowercase ASCII slug; unsupported characters become separators."""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(
        char for char in normalized if not unicodedata.combining(char)
    )
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")


def unique_lines(text: str, *, ignore_case: bool = False) -> str:
    """Keep the first occurrence of each line, preserving order and spelling.

    Normalize line endings to LF and preserve whether the input ends in a
    line separator. Whitespace within a line remains significant.
    """
    seen = set()
    result = []
    lines = text.splitlines()
    for value in lines:
        key = value.casefold() if ignore_case else value
        if key not in seen:
            seen.add(key)
            result.append(value)
    if not lines:
        return ""
    has_ending = text.endswith(("\n", "\r", "\v", "\f", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029"))
    return "\n".join(result) + ("\n" if has_ending else "")
