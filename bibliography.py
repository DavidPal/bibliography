# BibTeX bibliography beautifier.
#
# Author: David Pal <davidko.pal@gmail.com>
# Date: September 2013 -- September 2015
#
# Usage:
#
#   bibliography.py input.bib
#
# The script prints the formatted version on the console.
# To redirect into a file, use:
#
#   bibliography.py input.bib > output.bib

import sys
import re
import string

entry_types= {
               'article'       : 'Article',
	       'book'          : 'Book',
               'booklet'       : 'Booklet',
               # 'Conference' is the same as 'InProceedings'
               'conference'    : 'InProceedings',
               'inbook'        : 'InBook',
	       'incollection'  : 'InCollection',
               'inproceedings' : 'InProceedings',
               'manual'        : 'Manual',
               'mastersthesis' : 'MastersThesis',
               'misc'          : 'Misc',
               'phdthesis'     : 'PhDThesis',
               'proceedings'   : 'Proceedings',
               'techreport'    : 'TechReport',
               'unpublished'   : 'Unpublished',
               'string'        : 'String',
	      }

def Format(text):
	return ' '.join(text.split())

def CamelCase(text):
	word_start = True
	s = ''
	for c in text.lower():
		if word_start:
			c = c.upper()
		word_start = not c.isalpha()
		s = s + c
	return s

def FindMatchingParenthesis(text):
	nesting = 1
	end = 0
	for i in range(1, len(text)):
		if text[i] == '{':
			nesting = nesting + 1
		elif text[i] == '}':
			nesting = nesting - 1
		end = i
		if nesting == 0:
			break
	end = end + 1
	return (text[:end], text[end:])

def RemoveBraces(text):
	text = text.strip()
	if text[0] in ['{', '\"']:
		 text = text[1:]
	if text[-1] in ['}', '\"']:
		 text = text[:-1]
	return text

def NormalizeAuthor(text):
	parts = text.split(',', 1)
	if len(parts) >= 2:
		return parts[1].strip() + ' ' + parts[0].strip()
	return parts[0].strip()

def NormalizeAuthors(text):
	text = RemoveBraces(text)
	authors = text.split(' and ')
	return '{' + ' and '.join([NormalizeAuthor(author) for author in authors]) + '}'

def NormalizePages(text):
	text = RemoveBraces(text)
	parts = text.split('--', 1)
	if not '--' in text:
		parts = text.split('-', 1)
	normalized = parts[0].strip()
	if len(parts) >= 2:
		normalized = parts[0].strip() + "--" + parts[1].strip()
	return '{' + normalized + '}'


# An entry object
class Entry(object):
	def __init__(self):
		self.entry_type = 'UNKNOWN'
		self.entry_name = ''
		self.rows = { }

	def ParseFromString(self, text):
		m = re.match('\s*@\s*(\w+)\s*({)\s*', text)
		if not m:
			return None
		self.entry_type = m.group(1)
		self.entry_type = self.NormalizedEntryType()
		text = text[m.end(2):]
		text, rest = FindMatchingParenthesis(text)

		m = re.match('\s*([-:\w]+)\s*,\s*', text)
		if m:
			self.entry_name = m.group(1)
			text = text[m.end():]

		while text:
			text = self.ParseRow(text)
		return rest

	def ParseRow(self, text):
		m = re.match('\s*,?\s*([\w-]+)\s*=\s*', text)
		if not m:
			return None
		key = m.group(1)
		if not self.entry_type == 'String':
			key = CamelCase(key)
		text = text[m.end():]

		if text[0] == '{':
			text, rest = FindMatchingParenthesis(text)
			self.rows[key] = text
		elif text[0] == '\"':
			m = re.match('("[^\"]+")\s*,?\s*', text)
			self.rows[key] = m.group(1)
			rest = text[m.end():]
		else:
			m = re.match('\s*(\w+)\s*,?\s*', text)
			rest = text[m.end():]
			value = m.group(1)
			if re.match('^[0-9]*$', value):
				self.rows[key] = '{' + value + '}'
			else:
				self.rows[key] = value

		return rest



	def NormalizedEntryType(self):
		entry_type = self.entry_type.lower()
		if entry_type in entry_types:
			entry_type = entry_types[entry_type]
		return entry_type

	def ToString(self):
		s = '@' + self.entry_type + '{'
		if self.entry_name:
			s += self.entry_name + ','
		s += '\n'
		keys = sorted(self.rows.keys())
		for key in keys:
			s += + 4*' '
			s += key
			s += max(0, 13-len(key))*' '
			s += ' = '
			value = self.rows[key]
			if (not self.entry_type == 'String'):
				if (key in ['Author', 'Editor']):
					value = NormalizeAuthors(value)
				if (key == 'Pages'):
					value = NormalizePages(value)
			s += Format(value)
			if self.entry_type != 'String':
				s += ','
			s += '\n'
		return s + '}\n'

	def SortKey(self):
		priorities = {
               		'String'        : -99,
               		'Proceedings'   : 99,
               		'Book'          : 99,
	      	}
		if self.entry_type in priorities:
			return priorities[self.entry_type]
		return 0



def ParseEntries(text):
	entries = []
	while True:
		e = Entry()
		text = e.ParseFromString(text)
		if not text:
			break
		entries.append(e)
	return entries

def SortEntries(entries):
	entries.sort(key=lambda e: e.entry_name)
	entries.sort(key=lambda e: e.entry_type)
	entries.sort(key=lambda e: e.SortKey())
	return entries


def ReadFile():
	lines = []
	with open(sys.argv[1], 'r') as f:
		for line in f:
			if line.strip().startswith('%'):
				print(line.strip())
			else:
				lines.append(line)
	text = '\n'.join(lines)
	return text

# main
text = ReadFile()
entries = ParseEntries(text)
entries = SortEntries(entries)
for entry in entries:
	print(entry.ToString())
