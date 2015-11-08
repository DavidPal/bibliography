#!/usr/bin/env python

import bibliography
import unittest

class TestBibliography(unittest.TestCase):

	def test_Format(self):
		self.assertEqual('hello world', bibliography.Format(' hello   \n world \r \t '))

	def test_Capitalize(self):
		self.assertEqual('Hello World', bibliography.Capitalize('hello world'))

	def test_RemoveBraces(self):
		self.assertEqual('hello world', bibliography.RemoveBraces('{hello world}'))

	def test_FindMatchingParenthesis(self):
		result1, result2 = bibliography.FindMatchingParenthesis('{hello {world} 123} END }')
		self.assertEqual('{hello {world} 123}', result1)
		self.assertEqual(' END }', result2)

	def test_SafeParseInt(self):
		self.assertEqual(123, bibliography.SafeParseInt('123'))
		self.assertEqual(None, bibliography.SafeParseInt('hello world'))

	def test_NormalizeAuthor(self):
		self.assertEqual('David Pal', bibliography.NormalizeAuthor('David Pal'))
		self.assertEqual('David Pal', bibliography.NormalizeAuthor('Pal, David'))

	def test_NormalizeAuthor(self):
		self.assertEqual('David Pal', bibliography.NormalizeAuthors('David Pal'))
		self.assertEqual('David Pal and Francesco Orabona', bibliography.NormalizeAuthors('Pal, David and Francesco Orabona'))

	def test_NormalizePages(self):
		self.assertEqual('123--456', bibliography.NormalizePages(' 123 -- 456 '))
		self.assertEqual('123--456', bibliography.NormalizePages('123-456'))
		self.assertEqual('123', bibliography.NormalizePages('123'))

	def test_NormalizeYear(self):
		self.assertEqual('1887', bibliography.NormalizeYear('1887'))
		self.assertEqual('1995', bibliography.NormalizeYear('  95 '))
		self.assertEqual('2015', bibliography.NormalizeYear('2015'))

	def test_NormalizeMonth(self):
		self.assertEqual('January', bibliography.NormalizeMonth('january'))
		self.assertEqual('April', bibliography.NormalizeMonth('apr'))
		self.assertEqual('September', bibliography.NormalizeMonth('sept'))
		self.assertEqual('December', bibliography.NormalizeMonth('decem'))
		self.assertEqual('unknown month', bibliography.NormalizeMonth('unknown month'))


if __name__ == '__main__':
	unittest.main()
