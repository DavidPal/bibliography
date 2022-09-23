#!/usr/bin/env python

"""Unit tests for bibliography module."""

import unittest

import bibliography


class TestBibliography(unittest.TestCase):
    """Unit tests for bibliography module."""

    def test_format_text(self):
        """Tests format_text() function."""
        self.assertEqual("hello world", bibliography.format_text(" hello   \n world \r \t "))

    def test_capitalize(self):
        """Tests capitalize() function."""
        self.assertEqual("Hello World", bibliography.capitalize("hello world"))

    def test_remove_braces(self):
        """Tests remove_braces() function."""
        self.assertEqual("hello world", bibliography.remove_braces("{hello world}"))

    def test_find_matching_parenthesis(self):
        """Tests find_matching_closing_brace() function."""
        result1, result2 = bibliography.find_matching_closing_brace("{hello {world} 123} END }")
        self.assertEqual("{hello {world} 123}", result1)
        self.assertEqual(" END }", result2)

    def test_safe_parse_int(self):
        """Tests safe_parse_int() function."""
        self.assertEqual(123, bibliography.safe_parse_int("123"))
        self.assertEqual(None, bibliography.safe_parse_int("hello world"))

    def test_normalize_author(self):
        """Tests normalize_author() function."""
        self.assertEqual("David", bibliography.normalize_author("David"))
        self.assertEqual("David", bibliography.normalize_author("  David  "))
        self.assertEqual("David Pal", bibliography.normalize_author("  David   Pal  "))
        self.assertEqual("David Pal", bibliography.normalize_author("Pal, David"))
        self.assertEqual("Paul R. Halmos", bibliography.normalize_author(" Halmos ,  Paul   R. "))
        self.assertEqual(
            "David Pal and Francesco Orabona",
            bibliography.normalize_authors("Pal, David and Francesco Orabona"),
        )

    def test_normalize_pages(self):
        """Tests normalize_pages() function."""
        self.assertEqual("123--456", bibliography.normalize_pages(" 123 -- 456 "))
        self.assertEqual("123--456", bibliography.normalize_pages("123-456"))
        self.assertEqual("123--456", bibliography.normalize_pages("  123  -  456  "))
        self.assertEqual("123", bibliography.normalize_pages("123"))

    def test_normalize_year(self):
        """Tests normalize_year() function."""
        self.assertEqual("not_a_year", bibliography.normalize_year("  not_a_year  "))
        self.assertEqual("2019", bibliography.normalize_year("  2019  "))
        self.assertEqual("1887", bibliography.normalize_year("1887"))
        self.assertEqual("1995", bibliography.normalize_year("  95 "))
        self.assertEqual("2015", bibliography.normalize_year("2015"))

    def test_normalize_month(self):
        """Tests normalize_month() function."""
        self.assertEqual("January", bibliography.normalize_month("january"))
        self.assertEqual("April", bibliography.normalize_month("apr"))
        self.assertEqual("September", bibliography.normalize_month("sept"))
        self.assertEqual("December", bibliography.normalize_month("decem"))
        self.assertEqual("unknown month", bibliography.normalize_month("unknown month"))

    def test_normalize_entry_type(self):
        """Tests normalize_entry_type() function."""
        self.assertEqual("Book", bibliography.normalize_entry_type("book"))
        self.assertEqual("Article", bibliography.normalize_entry_type("  artIclE "))
        self.assertEqual("InProceedings", bibliography.normalize_entry_type("conference"))
        self.assertEqual("unknown", bibliography.normalize_entry_type("  unknown"))


if __name__ == "__main__":
    unittest.main()
