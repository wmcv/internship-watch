import tempfile
import unittest
from pathlib import Path

from job_filters import wanted_location, wanted_title
from parse_boards import parse_rows


class FilterTests(unittest.TestCase):
    def test_software_intern_is_included(self):
        self.assertTrue(wanted_title("Software Engineering Intern"))

    def test_non_engineering_intern_is_excluded(self):
        self.assertFalse(wanted_title("Product Management Intern"))

    def test_us_and_canada_are_included(self):
        self.assertTrue(wanted_location("Seattle, WA"))
        self.assertTrue(wanted_location("Halifax, NS, Canada"))

    def test_foreign_location_is_excluded(self):
        self.assertFalse(wanted_location("London, UK"))


class SimplifyParserTests(unittest.TestCase):
    def test_offseason_term_is_parsed(self):
        board = """
## 💻 Software Engineering Internship Roles
<tr><td><a href="https://simplify.jobs/c/Example">Example</a></td>
<td>Software Engineer Intern</td><td>Toronto, ON, Canada</td>
<td>Winter 2027</td><td><a href="https://example.com/apply"><img alt="Apply"></a></td>
<td>0d</td></tr>
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "board.md"
            path.write_text(board, encoding="utf-8")
            rows = parse_rows(str(path))
        self.assertEqual(len(rows), 1)
        self.assertEqual(next(iter(rows.values()))["term"], "Winter 2027")


if __name__ == "__main__":
    unittest.main()
