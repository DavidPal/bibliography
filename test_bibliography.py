#!/usr/bin/env python

import bibliography
import unittest


class TestBibliography(unittest.TestCase):

	def test_format_text(self):
		self.assertEqual('hello world', bibliography.format_text(' hello   \n world \r \t '))

	def test_capitalize(self):
		self.assertEqual('Hello World', bibliography.capitalize('hello world'))

	def test_remove_braces(self):
		self.assertEqual('hello world', bibliography.remove_braces('{hello world}'))

	def test_find_matching_parenthesis(self):
		result1, result2 = bibliography.find_matching_parenthesis('{hello {world} 123} END }')
		self.assertEqual('{hello {world} 123}', result1)
		self.assertEqual(' END }', result2)

	def test_safe_parse_int(self):
		self.assertEqual(123, bibliography.safe_parse_int('123'))
		self.assertEqual(None, bibliography.safe_parse_int('hello world'))

	def test_normalize_author(self):
		self.assertEqual('David', bibliography.normalize_author('David'))
		self.assertEqual('David', bibliography.normalize_author('  David  '))
		self.assertEqual('David Pal', bibliography.normalize_author('  David   Pal  '))
		self.assertEqual('David Pal', bibliography.normalize_author('Pal, David'))
		self.assertEqual('Paul R. Halmos', bibliography.normalize_author(' Halmos ,  Paul   R. '))
		self.assertEqual('David Pal and Francesco Orabona', bibliography.normalize_authors('Pal, David and Francesco Orabona'))

	def test_normalize_pages(self):
		self.assertEqual('123--456', bibliography.normalize_pages(' 123 -- 456 '))
		self.assertEqual('123--456', bibliography.normalize_pages('123-456'))
		self.assertEqual('123--456', bibliography.normalize_pages('  123  -  456  '))
		self.assertEqual('123', bibliography.normalize_pages('123'))

	def test_normalize_year(self):
		self.assertEqual('not_a_year', bibliography.normalize_year('  not_a_year  '))
		self.assertEqual('2019', bibliography.normalize_year('  2019  '))
		self.assertEqual('1887', bibliography.normalize_year('1887'))
		self.assertEqual('1995', bibliography.normalize_year('  95 '))
		self.assertEqual('2015', bibliography.normalize_year('2015'))

	def test_normalize_month(self):
		self.assertEqual('January', bibliography.normalize_month('january'))
		self.assertEqual('April', bibliography.normalize_month('apr'))
		self.assertEqual('September', bibliography.normalize_month('sept'))
		self.assertEqual('December', bibliography.normalize_month('decem'))
		self.assertEqual('unknown month', bibliography.normalize_month('unknown month'))


if __name__ == '__main__':
	unittest.main()
