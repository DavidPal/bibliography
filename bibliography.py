#!/usr/bin/env python

"""BibTeX bibliography beautifier.

Author: David Pal <davidko.pal@gmail.com>
Date: 2013-2023

Usage:

   bibliography.py file.bib

The script formats the bibliographic file. The script overwrites the input file.
If you do not want the input file to be overwritten, use --output option:

   bibliography.py file.bib --output output.bib

"""

import argparse
import dataclasses
import re
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

# Dictionary mapping lower-case type of bibliographic entry to its proper spelling.
ENTRY_TYPES = {
    "article": "Article",
    "book": "Book",
    "booklet": "Booklet",
    "conference": "InProceedings",  # "Conference" is the same as "InProceedings"
    "inbook": "InBook",
    "incollection": "InCollection",
    "inproceedings": "InProceedings",
    "manual": "Manual",
    "mastersthesis": "MastersThesis",
    "misc": "Misc",
    "phdthesis": "PhDThesis",
    "proceedings": "Proceedings",
    "techreport": "TechReport",
    "unpublished": "Unpublished",
    "string": "String",
}

# Dictionary mapping entry type to their priority.
# Entries not listed have priority zero.
ENTRY_PRIORITIES = {
    "String": -99,
    "Proceedings": 99,
    "Book": 99,
}

# Dictionary mapping a lower-case 3 letter prefix of a calendar month
# to its proper spelling.
MONTHS = {
    "jan": "January",
    "feb": "February",
    "mar": "March",
    "apr": "April",
    "may": "May",
    "jun": "June",
    "jul": "July",
    "aug": "August",
    "sep": "September",
    "oct": "October",
    "nov": "November",
    "dec": "December",
}


def format_text(text):
    """Removes unnecessary white space between words."""
    return " ".join(text.split())


def capitalize(text):
    """Capitalizes initial letters in words in a string."""
    word_start = True
    output = ""
    for char in text.lower():
        if word_start:
            char = char.upper()
        word_start = not char.isalpha()
        output += char
    return output


def find_matching_closing_brace(text: str) -> Tuple[str, str]:
    """Finds closing brace in a string that matches '{' + string."""
    nesting = 1
    end = 0
    for i in range(1, len(text)):
        if text[i] == "{":
            nesting = nesting + 1
        elif text[i] == "}":
            nesting = nesting - 1
        end = i
        if nesting == 0:
            break
    end = end + 1
    return text[:end], text[end:]


def remove_braces(text: str) -> str:
    """Removes opening brace from the beginning and closing brace from the end of a string."""
    if text[0] == "{":
        text = text[1:]
    if text[-1] == "}":
        text = text[:-1]
    return text


def normalize_author(text: str) -> str:
    """Puts an authors name into canonical form."""
    parts = text.split(",", 1)
    if len(parts) >= 2:
        return format_text(parts[1]) + " " + format_text(parts[0].strip())
    return format_text(parts[0])


def normalize_authors(text: str) -> str:
    """Puts a list of authors' names into canonical form."""
    authors = text.split(" and ")
    return " and ".join([normalize_author(author) for author in authors])


def normalize_pages(text: str) -> str:
    """Puts the pages field into the canonical form."""
    parts = text.split("--", 1)
    if "--" not in text:
        parts = text.split("-", 1)
    normalized = parts[0].strip()
    if len(parts) >= 2:
        normalized = parts[0].strip() + "--" + parts[1].strip()
    return normalized


def safe_parse_int(text: str) -> Optional[int]:
    """Converts string to an integer or returns None if that is not possible."""
    try:
        return int(text)
    except ValueError:
        return None


def normalize_year(text: str) -> str:
    """Puts year into canonical form."""
    year = safe_parse_int(text)
    if not year:
        return text.strip()
    if 10 <= year <= 99:
        return str(1900 + year)
    return str(year)


def normalize_month(text: str) -> str:
    """Puts name of a month into canonical form."""
    prefix = text[:3].lower()
    if prefix in MONTHS:
        return MONTHS[prefix]
    return text


def normalize_entry_type(entry_type: str) -> str:
    """Puts the type of entry into canonical form."""
    entry_type = entry_type.strip().lower()
    if entry_type not in ENTRY_TYPES:
        return entry_type
    return ENTRY_TYPES[entry_type]


@dataclasses.dataclass
class Entry:
    """Entry represents a bibliographic entry."""

    entry_type: str = "UNKNOWN"
    entry_name: str = ""
    fields: Dict[str, str] = dataclasses.field(default_factory=dict)

    def parse_from_string(self, text: str) -> Optional[str]:
        """Parses the entry from a string that appears first in the string."""
        match = re.match("\\s*@\\s*(\\w+)\\s*({)\\s*", text)
        if not match:
            return None
        self.entry_type = match.group(1)
        self.entry_type = normalize_entry_type(self.entry_type)
        text = text[match.end(2) :]
        text, rest = find_matching_closing_brace(text)

        match = re.match("\\s*([^\\s]+)\\s*,\\s*", text)
        if match:
            self.entry_name = match.group(1)
            text = text[match.end() :]

        while text:
            text = self.parse_field(text)  # type: ignore[assignment]
        return rest

    def parse_field(self, text: str) -> Optional[str]:
        """Parses the field of an entry from a string that appears first in the string."""
        match = re.match("\\s*,?\\s*([\\w-]+)\\s*=\\s*", text)
        if not match:
            return None
        key = match.group(1)
        if self.entry_type != "String":
            key = capitalize(key)
        text = text[match.end() :]

        value = ""
        if text[0] == "{":
            value, rest = find_matching_closing_brace(text)
            value = remove_braces(value)
        elif text[0] == '"':
            match = re.match('^"([^"]+)"\\s*,?\\s*', text)
            value = match.group(1)  # type: ignore[union-attr]
            rest = text[match.end() :]  # type: ignore[union-attr]
        else:
            match = re.match("\\s*(\\w+)\\s*,?\\s*", text)
            value = match.group(1)  # type: ignore[union-attr]
            rest = text[match.end() :]  # type: ignore[union-attr]

        self.fields[key] = value.strip()
        return rest

    def __str__(self):
        """Returns the BibTeX representation of the entry."""
        output = "@" + self.entry_type + "{"
        if self.entry_name:
            output += self.entry_name + ","
        output += "\n"
        keys = sorted(self.fields.keys())
        for key in keys:
            output += 4 * " "
            output += key
            output += max(0, 13 - len(key)) * " "
            output += " = "
            value = self.fields[key]
            if self.entry_type != "String":
                if key in ["Author", "Editor"]:
                    value = normalize_authors(value)
                if key == "Pages":
                    value = normalize_pages(value)
                if key == "Year":
                    value = normalize_year(value)
                if key == "Month":
                    value = normalize_month(value)

            output += "{" + format_text(value) + "}"
            if self.entry_type != "String":
                output += ","
            output += "\n"
        return output + "}"

    def priority(self):
        """Returns the sort priority of the entry."""
        if self.entry_type in ENTRY_PRIORITIES:
            return ENTRY_PRIORITIES[self.entry_type]
        return 0


def parse_entries(text: str) -> List[Entry]:
    """Parses a list of bibliographic entries from a string."""
    entries = []
    while True:
        entry = Entry()
        text = entry.parse_from_string(text)  # type: ignore[assignment]
        if not text:
            break
        entries.append(entry)
    return entries


def read_file(file_name: str) -> Tuple[List[str], str]:
    """Reads content of a bibliography file."""
    comments = []
    lines = []
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip().startswith("%"):
                comments.append(line.strip())
            else:
                lines.append(line)
    text = "\n".join(lines)
    return comments, text


def write_file(file_name: str, comments: List[str], entries: List[Entry]) -> None:
    """Writes text into a file."""
    with open(file_name, "w", encoding="utf-8") as file:
        if comments:
            file.write("\n".join(comments))
            file.write("\n")
        file.write("\n\n".join(str(entry) for entry in entries))
        file.write("\n")


def main():
    """Reads the input bibliography file and outputs its properly formatted version."""
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="bibliographic file")
    parser.add_argument("--output", help="output file")
    parsed_arguments = parser.parse_args()

    print(f"Reading file '{parsed_arguments.input}' ...")
    comments, text = read_file(parsed_arguments.input)
    print("Parsing entries...")
    entries = parse_entries(text)
    entries.sort(key=lambda entry: (entry.priority(), entry.entry_type, entry.entry_name))
    if parsed_arguments.output:
        output_file = parsed_arguments.output
    else:
        output_file = parsed_arguments.input
    print(f"Writing file '{output_file}' ...")
    write_file(output_file, comments, entries)


if __name__ == "__main__":
    main()
