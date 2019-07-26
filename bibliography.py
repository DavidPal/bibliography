#!/usr/bin/env python

# BibTeX bibliography beautifier.
#
# Author: David Pal <davidko.pal@gmail.com>
# Date: 2013-2019
#
# Usage:
#
#   bibliography.py input.bib
#
# The script prints the formatted version on the console.
# To redirect into a file, use:
#
#   bibliography.py input.bib > output.bib

import re
import sys

entry_types = {
    'article': 'Article',
    'book': 'Book',
    'booklet': 'Booklet',
    'conference': 'InProceedings',  # 'Conference' is the same as 'InProceedings'
    'inbook': 'InBook',
    'incollection': 'InCollection',
    'inproceedings': 'InProceedings',
    'manual': 'Manual',
    'mastersthesis': 'MastersThesis',
    'misc': 'Misc',
    'phdthesis': 'PhDThesis',
    'proceedings': 'Proceedings',
    'techreport': 'TechReport',
    'unpublished': 'Unpublished',
    'string': 'String',
}

months = {
    'jan': 'January',
    'feb': 'Februry',
    'mar': 'March',
    'apr': 'April',
    'may': 'May',
    'jun': 'June',
    'jul': 'July',
    'aug': 'August',
    'sep': 'September',
    'oct': 'October',
    'nov': 'November',
    'dec': 'December',
}


def format_text(text):
    return ' '.join(text.split())


def capitalize(text):
    word_start = True
    s = ''
    for c in text.lower():
        if word_start:
            c = c.upper()
        word_start = not c.isalpha()
        s = s + c
    return s


def find_matching_parenthesis(text):
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
    return text[:end], text[end:]


def remove_braces(text):
    if text[0] == '{':
        text = text[1:]
    if text[-1] == '}':
        text = text[:-1]
    return text


def normalize_author(text):
    parts = text.split(',', 1)
    if len(parts) >= 2:
        return format_text(parts[1]) + ' ' + format_text(parts[0].strip())
    return format_text(parts[0])


def normalize_authors(text):
    authors = text.split(' and ')
    return ' and '.join([normalize_author(author) for author in authors])


def normalize_pages(text):
    parts = text.split('--', 1)
    if '--' not in text:
        parts = text.split('-', 1)
    normalized = parts[0].strip()
    if len(parts) >= 2:
        normalized = parts[0].strip() + '--' + parts[1].strip()
    return normalized


def safe_parse_int(text):
    try:
        return int(text)
    except ValueError:
        return None


def normalize_year(text):
    year = safe_parse_int(text)
    if not year:
        return text.strip()
    if (year >= 10) and (year <= 99):
        return str(1900 + year)
    return str(year)


def normalize_month(text):
    prefix = text[:3].lower()
    if prefix in months:
        return months[prefix]
    return text


# An entry object
class Entry(object):
    def __init__(self):
        self.entry_type = 'UNKNOWN'
        self.entry_name = ''
        self.rows = {}

    def parse_from_string(self, text):
        m = re.match('\\s*@\\s*(\\w+)\\s*({)\\s*', text)
        if not m:
            return None
        self.entry_type = m.group(1)
        self.entry_type = self.normalized_entry_type()
        text = text[m.end(2):]
        text, rest = find_matching_parenthesis(text)

        m = re.match('\\s*([^\\s]+)\\s*,\\s*', text)
        if m:
            self.entry_name = m.group(1)
            text = text[m.end():]

        while text:
            text = self.parse_row(text)
        return rest

    def parse_row(self, text):
        m = re.match('\\s*,?\\s*([\\w-]+)\\s*=\\s*', text)
        if not m:
            return None
        key = m.group(1)
        if not self.entry_type == 'String':
            key = capitalize(key)
        text = text[m.end():]

        value = ''
        if text[0] == '{':
            value, rest = find_matching_parenthesis(text)
            value = remove_braces(value)
        elif text[0] == '\"':
            m = re.match('^"([^\"]+)"\\s*,?\\s*', text)
            value = m.group(1)
            rest = text[m.end():]
        else:
            m = re.match('\\s*(\\w+)\\s*,?\\s*', text)
            value = m.group(1)
            rest = text[m.end():]

        self.rows[key] = value.strip()
        return rest

    def normalized_entry_type(self):
        entry_type = self.entry_type.lower()
        if entry_type in entry_types:
            entry_type = entry_types[entry_type]
        return entry_type

    def __str__(self):
        s = '@' + self.entry_type + '{'
        if self.entry_name:
            s += self.entry_name + ','
        s += '\n'
        keys = sorted(self.rows.keys())
        for key in keys:
            s += + 4 * ' '
            s += key
            s += max(0, 13 - len(key)) * ' '
            s += ' = '
            value = self.rows[key]
            if not self.entry_type == 'String':
                if key in ['Author', 'Editor']:
                    value = normalize_authors(value)
                if key == 'Pages':
                    value = normalize_pages(value)
                if key == 'Year':
                    value = normalize_year(value)
                if key == 'Month':
                    value = normalize_month(value)

            s += '{' + format_text(value) + '}'
            if self.entry_type != 'String':
                s += ','
            s += '\n'
        return s + '}'

    def sort_key(self):
        priorities = {
            'String': -99,
            'Proceedings': 99,
            'Book': 99,
        }
        if self.entry_type in priorities:
            return priorities[self.entry_type]
        return 0


def parse_entries(text):
    entries = []
    while True:
        e = Entry()
        text = e.parse_from_string(text)
        if not text:
            break
        entries.append(e)
    return entries


def sort_entries(entries):
    entries.sort(key=lambda e: e.entry_name)
    entries.sort(key=lambda e: e.entry_type)
    entries.sort(key=lambda e: e.sort_key())
    return entries


def read_file():
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
def main():
    text = read_file()
    entries = parse_entries(text)
    entries = sort_entries(entries)
    print("\n\n".join(str(entry) for entry in entries))


if __name__ == '__main__':
    main()
