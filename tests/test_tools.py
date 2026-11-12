import unittest

from pocket_text_tools import TextStats, count_text, slugify, unique_lines


class TextToolsTests(unittest.TestCase):
    def test_counts_empty_and_unicode_text(self):
        self.assertEqual(count_text(""), TextStats(0, 0, 0))
        self.assertEqual(count_text("café world\nnext\n"), TextStats(16, 3, 2))

    def test_slug_accents_and_separators(self):
        self.assertEqual(slugify("  Café & Déjà Vu! "), "cafe-deja-vu")
        self.assertEqual(slugify("hello世界there"), "hello-there")
        self.assertEqual(slugify("!!!"), "")

    def test_unique_lines_preserves_order_and_whitespace(self):
        self.assertEqual(unique_lines("b\na\nb\n a"), "b\na\n a")

    def test_unique_lines_handles_endings_and_empty_lines(self):
        self.assertEqual(unique_lines("a\r\na\r\n\r\n"), "a\n\n")
        self.assertEqual(unique_lines(""), "")
        self.assertEqual(unique_lines("\n\n"), "\n")

    def test_casefold_preserves_first_spelling(self):
        self.assertEqual(unique_lines("Straße\nSTRASSE\n", ignore_case=True), "Straße\n")
        self.assertEqual(unique_lines("A\na"), "A\na")


if __name__ == "__main__":
    unittest.main()
