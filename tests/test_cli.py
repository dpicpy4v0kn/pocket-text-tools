import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def run_cli(self, *args, data=b""):
        return subprocess.run(
            [sys.executable, "-m", "pocket_text_tools", *args],
            input=data, capture_output=True, check=False,
        )

    def test_stats_from_stdin(self):
        result = self.run_cli("stats", data="café\n".encode())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"characters": 5, "words": 1, "lines": 1})

    def test_slug_from_file(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.txt"
            source.write_text("Café time!", encoding="utf-8")
            result = self.run_cli("slug", str(source))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"cafe-time\n")

    def test_unique_preserves_missing_final_newline(self):
        result = self.run_cli("unique", "--ignore-case", data=b"One\r\none\r\nTwo")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"One\nTwo")

    def test_invalid_utf8_has_useful_error(self):
        result = self.run_cli("stats", data=b"\xff")
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"pocket-text-tools:", result.stderr)
        self.assertNotIn(b"Traceback", result.stderr)

    def test_missing_file_has_useful_error(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_cli("stats", str(Path(directory) / "missing.txt"))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, b"")
        self.assertNotIn(b"Traceback", result.stderr)

    def test_command_is_required(self):
        self.assertEqual(self.run_cli().returncode, 2)
