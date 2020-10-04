#!/usr/bin/env python3

#  libcodepoint.py - Generates a C file with a Unicode lookup table.
#  Copyright (c) 2020 Henry G. Stratmann III
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import List, Dict, Iterable
import os
import sys
import csv
import urllib.request
import argparse

FILE_NAME = os.path.basename(sys.argv[0])
MAX_CODEPOINTS = 1114112  # Define by the Unicode Consortium.
BUCKET_SIZE = 128  # The number of codepoints in a single stage1 bucket.
UNICODE_VERSION = '13.0.0' # The unicode database version to download.

ALPHA_MASK = 0x01
DIGIT_MASK = 0x02
LOWER_MASK = 0x04
UPPER_MASK = 0x08
TITLE_MASK = 0x10
SPACE_MASK = 0x20
PRINTABLE_MASK = 0x40
PUNCTUATION_MASK = 0x80
CONTROL_MASK = 0x100
EMOJI_MASK = 0x200
LINEBREAK_MASK = 0x400
CONNECTING_MASK = 0x800
COMBINING_MASK = 0x1000
FORMATTING_MASK = 0x2000


class Codepoint:
    def __init__(self, upper: int, lower: int, title: int, digit: int, flags: int):
        self.upper = upper
        self.lower = lower
        self.title = title
        self.digit = digit
        self.flags = flags

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Codepoint):
            return NotImplemented
        if self.upper == other.upper and \
           self.lower == other.lower and \
           self.title == other.title and \
           self.digit == other.digit and \
           self.flags == other.flags:
            return True
        return False

    def __hash__(self) -> int:
        return (hash(self.upper) << 24) ^ (hash(self.lower) << 20) ^ (hash(self.title) << 16) ^ (hash(self.digit) << 8) ^ hash(self.flags)


class UnicodeDataRecord:
    def __init__(self, record: List[str]):
        # 15 fields from UnicodeData.txt
        # See: https://www.unicode.org/reports/tr44/#UnicodeData.txt
        self.codepoint = int(record[0], 16)
        self.name = record[1]
        self.category = record[2]
        self.canonical_combining_class = record[3]
        self.bidi_class = record[4]
        self.decomposition_type = record[5]
        self.decomposition_mapping = record[6]
        self.numeric_type = int(record[7]) if record[7] else 0
        self.numeric_value = record[8]
        self.bidi_mirrored = record[9]
        self.unicode_1_name = record[10]  # obsolete
        self.iso_comment = record[11]  # obsolete
        self.uppercase_mapping = int(record[12], 16) if record[12] else 0
        self.lowercase_mapping = int(record[13], 16) if record[13] else 0
        self.titlecase_mapping = int(record[14], 16) if record[14] else 0


def collect_code_points_from_unicode_database() -> Dict[int, Codepoint]:
    """
    This function downloads and gathers data on all the Unicode code points and returns the data in a dictionary.
    The dictionary key is the Unicode code point number and the value is information about the code point.
    """

    # First download the Unicode database from http://www.unicode.org
    # The Unicode Consortium provides CSV database with information on all code points.
    outdir = f"ucd-{UNICODE_VERSION}"
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    unicode_data_url = f'http://www.unicode.org/Public/{UNICODE_VERSION}/ucd/UnicodeData.txt'
    derived_core_properties_url = f'http://www.unicode.org/Public/{UNICODE_VERSION}/ucd/DerivedCoreProperties.txt'
    line_break_url = f'http://unicode.org/Public/{UNICODE_VERSION}/ucd/LineBreak.txt'
    emoji_data_url = f'http://unicode.org/Public/{UNICODE_VERSION}/ucd/emoji/emoji-data.txt'

    unicode_data_file = os.path.join(outdir, 'UnicodeData.txt')
    if not os.path.exists(unicode_data_file):
        urllib.request.urlretrieve(unicode_data_url, unicode_data_file)

    derived_core_properties_file = os.path.join(outdir, 'DerivedCoreProperties.txt')
    if not os.path.exists(derived_core_properties_file):
        urllib.request.urlretrieve(derived_core_properties_url, derived_core_properties_file)

    line_break_file = os.path.join(outdir, 'LineBreak.txt')
    if not os.path.exists(line_break_file):
        urllib.request.urlretrieve(line_break_url, line_break_file)

    emoji_data_file = os.path.join(outdir, 'emoji-data.txt')
    if not os.path.exists(emoji_data_file):
        urllib.request.urlretrieve(emoji_data_url, emoji_data_file)

    # This is the dictionary this function builds that will contain all Unicode Codepoints.
    # The key is the code point number and the value is information about the code point.
    codepoints: Dict[int, Codepoint] = {}

    # Python's CSV library lacks handling '#" comments.
    # This function will stip them out.
    def decomment(csvfile: Iterable[str]) -> Iterable[str]:
        for row in csvfile:
            raw = row.split('#')[0].strip()
            if raw:
                yield raw

    # Read all code points from the UnicodeData.txt file.
    with open(unicode_data_file, encoding='utf-8-sig') as file:
        reader = csv.reader(decomment(file), delimiter=';')
        for line in reader:
            record = UnicodeDataRecord(line)

            flags = 0
            if record.category in ['Lm', 'Lt', 'Lu', 'Ll', 'Lo', 'Nl']:
                flags |= ALPHA_MASK
            if record.category == 'Lt':
                flags |= TITLE_MASK
            if record.category == 'Zs':
                flags |= SPACE_MASK
            if record.category in ['Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po']:
                flags |= PUNCTUATION_MASK
            if record.category == 'Pc':
                flags |= CONNECTING_MASK
            if record.category in ['Mn', 'Mc']:
                flags |= COMBINING_MASK
            if record.category == 'Cf':
                flags |= FORMATTING_MASK
            if record.category == 'Cc':
                flags |= CONTROL_MASK
            if record.category[0] not in ['C', 'Z'] or record.codepoint == ord(' '):
                flags |= PRINTABLE_MASK
            if record.category in ['Nd', 'Nl']:
                flags |= DIGIT_MASK
            if record.category in ['Zl', 'Zp']:
                flags |= LINEBREAK_MASK

            # Count all the CJK Ideograph and Hangul Syllable ranges and
            # generate names
            if ('Ideograph' in record.name or record.name.startswith('<Hangul')) and record.name.endswith('First>'):
                next_line = next(reader)
                next_codepoint = int(next_line[0], 16)
                for i in range(record.codepoint, next_codepoint + 1):
                    codepoints[i] = Codepoint(record.uppercase_mapping, record.lowercase_mapping, record.titlecase_mapping, record.numeric_type, flags)
            else:
                codepoints[record.codepoint] = Codepoint(
                    record.uppercase_mapping, record.lowercase_mapping, record.titlecase_mapping, record.numeric_type, flags)

    # Gather additional case information from the DerivedCoreProperties.txt file.
    with open(derived_core_properties_file, encoding='utf-8-sig') as file:
        reader = csv.reader(decomment(file), delimiter=';')
        for line in reader:
            codepoint_range = line[0].split('..')
            properties = line[1].strip()

            if len(codepoint_range) > 1:
                first_codepoint = int(codepoint_range[0], 16)
                last_codepoint = int(codepoint_range[1], 16)
            else:
                first_codepoint = int(codepoint_range[0], 16)
                last_codepoint = first_codepoint

            for i in range(first_codepoint, last_codepoint + 1):
                if i in codepoints:
                    if properties == 'Lowercase':
                        codepoints[i].flags |= LOWER_MASK
                    elif properties == 'Uppercase':
                        codepoints[i].flags |= UPPER_MASK

    # Gather line seperator information from the LineBreak.txt file
    with open(line_break_file, encoding='utf-8-sig') as file:
        reader = csv.reader(decomment(file), delimiter=';')
        for line in reader:
            codepoint_range = line[0].split('..')
            properties = line[1].strip()

            if len(codepoint_range) > 1:
                first_codepoint = int(codepoint_range[0], 16)
                last_codepoint = int(codepoint_range[1], 16)
            else:
                first_codepoint = int(codepoint_range[0], 16)
                last_codepoint = first_codepoint

            for i in range(first_codepoint, last_codepoint + 1):
                if i in codepoints:
                    if properties in ['NL', 'LF', 'CR']:
                        codepoints[i].flags |= LINEBREAK_MASK

    # Gather additional case information from the emoji-data.txt file.
    # This file is only available for Unicode 13.0+
    with open(emoji_data_file, encoding='utf-8-sig') as file:
        reader = csv.reader(decomment(file), delimiter=';')
        for line in reader:
            codepoint_range = line[0].split('..')

            if len(codepoint_range) > 1:
                first_codepoint = int(codepoint_range[0], 16)
                last_codepoint = int(codepoint_range[1], 16)
            else:
                first_codepoint = int(codepoint_range[0], 16)
                last_codepoint = first_codepoint

            for i in range(first_codepoint, last_codepoint + 1):
                if i in codepoints:
                    codepoints[i].flags |= EMOJI_MASK

    return codepoints


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-stdint", help="prevents inclusion of the stdint.h header", action="store_true")
    parser.add_argument("--no-inline", help="prevents usage of the inline keyword", action="store_true")
    parser.add_argument("--prefix", type=str, default="", help="a string to prefix C functions with")
    parser.add_argument("--info", help="displays size information about the generated output", action="store_true")
    parser.add_argument("outfile", type=str, help="name of the output file")

    if len(sys.argv) < 2:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    codepoints = collect_code_points_from_unicode_database()

    # This dictionary is used to keep an ordered set of all unique code points.
    # Many of the code points within the Unicode code space have overlapping properties so
    # only unique code points need to be serialized.
    unique_codepoints: Dict[Codepoint, int] = {}

    # Add the 'null' (e.g. zero property values) code point to the set of unique code points.
    # This code point will be used when attempting to retrieve an invalid code point from the C API.
    unique_codepoints[Codepoint(0, 0, 0, 0, 0)] = 0

    # Now add all the code points to create an ordered set.
    for codepoint in codepoints.values():
        if codepoint not in unique_codepoints:
            unique_codepoints[codepoint] = len(unique_codepoints)

    # Build a Two-stage table for storing all code points.
    # This is recommended by Chapter 5.1 of The Unicode Standard.
    stage1: List[int] = []
    stage2: List[int] = []
    stage2_tables: List[List[int]] = []

    for code in range(MAX_CODEPOINTS):
        # Only build stage2 tables on bucket boundaries.
        if (code % BUCKET_SIZE) != 0:
            continue

        # Build a stage2 table for the current range of codepoints.
        # This table may be discarded if it's a duplicate of another table.
        stage2_table = []

        for code2 in range(code, code + BUCKET_SIZE):
            if code2 in codepoints:
                codepoint = codepoints[code2] # Grab the codepoint.
                if codepoint in unique_codepoints: # Find its index within the ordered set of code points.
                    stage2_table += [unique_codepoints[codepoint]]
                    continue

            # Only a subset of the avaiable Unicode character space is mapped to real characters.
            # The current codepoint happens to not exists so default to the null codepoint.
            stage2_table += [0]

        if stage2_table in stage2_tables:
            stage1 += [stage2_tables.index(stage2_table) * BUCKET_SIZE]
        else:
            stage1 += [len(stage2)]
            stage2 += stage2_table
            stage2_tables += [stage2_table]

    if args.info:
        print('Total code points: %d' % (len(codepoints)))
        print('Unique code points: %d' % (len(unique_codepoints)))
        print('')

    with open(args.outfile, 'w') as file:
        code_points_size = (len(unique_codepoints) * 20) / 1024
        stage1_table_size = (len(stage1) * 4) / 1024
        stage2_table_size = (len(stage2) * 4) / 1024
        total_size = code_points_size + stage1_table_size + stage2_table_size

        if args.info:
            print(
                'Uncompressed code points table size: %d kilobytes' % ((len(codepoints) * 20) / 1024))
            print('Compressed code points table size: %d kilobytes' % (code_points_size))
            print('Stage1 table size: %d kilobytes' % (stage1_table_size))
            print('Stage2 table size: %d kilobytes' % (stage2_table_size))
            print('')
            print('Total compressed size: %d kilobytes' % (total_size))

        file.write('// Do NOT edit this file.\n')
        file.write('// This file was programmatically generated by %s\n' % (FILE_NAME))
        file.write('// It contains %d kilobytes of data.\n' % (total_size))
        file.write('\n')

        if args.no_stdint:
            code_point_type = 'long'
        else:
            file.write('#include <stdint.h>\n')
            file.write('\n')
            code_point_type = 'int32_t'

        prefix = args.prefix
        prefix_upper = prefix.upper()

        file.write('// ---------------------------------------------\n')
        file.write('// Start of Public Interface\n')
        file.write('// ---------------------------------------------\n')

        file.write('\n')
        file.write(f'#ifndef CODEPOINT_DEFINITIONS\n')
        file.write(f'#define CODEPOINT_DEFINITIONS\n')
        file.write('\n')

        file.write(f'typedef {code_point_type} {prefix}codepoint;\n')
        file.write('\n')

        file.write(f'{prefix}codepoint {prefix}codepoint_tolower({prefix}codepoint character);\n')
        file.write(f'{prefix}codepoint {prefix}codepoint_toupper({prefix}codepoint character);\n')
        file.write(f'{prefix}codepoint {prefix}codepoint_totitle({prefix}codepoint character);\n')
        file.write(f'int {prefix}codepoint_todigit({prefix}codepoint character);\n')
        file.write(f'long {prefix}codepoint_toflags({prefix}codepoint character);\n')
        file.write('\n')
        file.write(f'int {prefix}codepoint_islower({prefix}codepoint character);\n')
        file.write(f'int {prefix}codepoint_isupper({prefix}codepoint character);\n')
        file.write(f'int {prefix}codepoint_istitle({prefix}codepoint character);\n')
        file.write(f'int {prefix}codepoint_isdigit({prefix}codepoint character);\n')
        file.write(f'int {prefix}codepoint_isspace({prefix}codepoint character);\n')
        file.write(f'int {prefix}codepoint_iscntrl({prefix}codepoint character);\n')
        file.write(f'int {prefix}codepoint_ispunct({prefix}codepoint character);\n')
        file.write(f'int {prefix}codepoint_isemoji({prefix}codepoint character);\n')
        file.write(f'int {prefix}codepoint_isprint({prefix}codepoint character);\n')
        file.write(f'int {prefix}codepoint_isalpha({prefix}codepoint character);\n')
        file.write(f'int {prefix}codepoint_isalnum({prefix}codepoint character);\n')
        file.write(f'int {prefix}codepoint_isvalid({prefix}codepoint character);\n')

        # Write masks.
        file.write('\n')
        file.write(f"#define {prefix_upper}CODEPOINT_ALPHA 0x%0X // Unicode character classes 'Lm', 'Lt', 'Lu', 'Ll', 'Lo', 'Nl'\n" % (ALPHA_MASK))
        file.write(f"#define {prefix_upper}CODEPOINT_DIGIT 0x%0X // Unicode character classes 'Nd', 'Nl'\n" % (DIGIT_MASK))
        file.write(f'#define {prefix_upper}CODEPOINT_LOWER 0x%0x\n' % (LOWER_MASK))
        file.write(f'#define {prefix_upper}CODEPOINT_UPPER 0x%0x\n' % (UPPER_MASK))
        file.write(f"#define {prefix_upper}CODEPOINT_TITLE 0x%0x // Unicode character class 'Lt'\n" % (TITLE_MASK))
        file.write(f"#define {prefix_upper}CODEPOINT_SPACE 0x%0x // Unicode character class 'Zs'\n" % (SPACE_MASK))
        file.write(f'#define {prefix_upper}CODEPOINT_PRINTABLE 0x%0x\n' % (PRINTABLE_MASK))
        file.write(f"#define {prefix_upper}CODEPOINT_PUNCTUATION 0x%0x // Unicode character classes 'Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'\n" % (PUNCTUATION_MASK))
        file.write(f"#define {prefix_upper}CODEPOINT_CONTROL 0x%0x // Unicode character class 'Cc'\n" % (CONTROL_MASK))
        file.write(f'#define {prefix_upper}CODEPOINT_EMOJI 0x%0x\n' % (EMOJI_MASK))
        file.write(f'#define {prefix_upper}CODEPOINT_LINEBREAK 0x%0x\n' % (LINEBREAK_MASK))
        file.write(f"#define {prefix_upper}CODEPOINT_CONNECTING 0x%0x // Unicode character class 'Pc'\n" % (CONNECTING_MASK))
        file.write(f"#define {prefix_upper}CODEPOINT_COMBINING 0x%0x // Unicode character classes 'Mn', 'Mc'\n" % (COMBINING_MASK))
        file.write(f"#define {prefix_upper}CODEPOINT_FORMATTING 0x%0x // Unicode character class 'Cf'\n" % (FORMATTING_MASK))

        file.write('\n')
        file.write(f'#endif\n')  # end of definitions
        file.write('\n')

        file.write('// ---------------------------------------------\n')
        file.write('// End of Public Interface\n')
        file.write('// ---------------------------------------------\n')

        file.write('\n')
        # beginning of implementation
        file.write(f'#ifdef CODEPOINT_IMPLEMENTATION\n')
        file.write('\n')

        # Write unique codepoints.
        file.write('// This table is a set of %d unique code points.\n' % (len(unique_codepoints)))
        file.write('// It is %d bytes in size.\n' % (len(unique_codepoints) * 20))
        file.write(f'static const struct {prefix}codepointdata {{\n')
        file.write(f'    {prefix}codepoint upper;\n')
        file.write(f'    {prefix}codepoint lower;\n')
        file.write(f'    {prefix}codepoint title;\n')
        file.write('    int numeric_value;\n')
        file.write(f'    {code_point_type} flags;\n')
        file.write('} unicode_codepoints[] = {\n')
        for record in unique_codepoints:
            file.write('    {%d, %d, %d, %d, %d},\n' % (record.upper, record.lower, record.title, record.digit, record.flags))
        file.write('};\n\n')

        # Write stage1 table.
        file.write(f'static const {prefix}codepoint stage1_table[] = {{')
        for index, value in enumerate(stage1):
            if (index % 8) == 0:
                file.write('\n')
                file.write('    ')
            file.write('%d, ' % (value))
        file.write('\n')
        file.write('};\n\n')

        # Write stage2 table.
        file.write(f'static const {prefix}codepoint stage2_table[] = {{')
        for index, value in enumerate(stage2):
            if (index % 8) == 0:
                file.write('\n')
                file.write('    ')
            file.write('%d, ' % (value))
        file.write('\n')
        file.write('};\n\n')

        # If the inline keyword is enabled, then generate the following function with it.
        inline_keyword = '' if args.no_inline else 'inline '

        # Write helper function.
        file.write(f'static {inline_keyword}const struct {prefix}codepointdata *{prefix}getcodepointdata({prefix}codepoint ch) {{\n')
        file.write('    if (ch >= %d) {\n' % (MAX_CODEPOINTS))
        file.write('        return &unicode_codepoints[0]; // code point out of range\n')
        file.write('    }\n')
        file.write('    const int stage2_offset = stage1_table[ch / %d];\n' % (BUCKET_SIZE))
        file.write('    const int codepoint_index = stage2_table[stage2_offset + (ch %% %d)];\n' % (BUCKET_SIZE))
        file.write('    return &unicode_codepoints[codepoint_index];\n')
        file.write('}\n\n')

        # Write API functions.
        file.write(f'{prefix}codepoint {prefix}codepoint_tolower({prefix}codepoint character) {{\n')
        file.write(f'    const {prefix}codepoint cp = {prefix}getcodepointdata(character)->lower;\n')
        file.write('    return (cp == 0) ? character : cp;\n')
        file.write('}\n\n')

        file.write(f'{prefix}codepoint {prefix}codepoint_toupper({prefix}codepoint character) {{\n')
        file.write(f'    const {prefix}codepoint cp = {prefix}getcodepointdata(character)->upper;\n')
        file.write('    return (cp == 0) ? character : cp;\n')
        file.write('}\n\n')

        file.write(f'{prefix}codepoint {prefix}codepoint_totitle({prefix}codepoint character) {{\n')
        file.write(f'    const {prefix}codepoint cp = {prefix}getcodepointdata(character)->title;\n')
        file.write('    return (cp == 0) ? character : cp;\n')
        file.write('}\n\n')

        file.write(f'int {prefix}codepoint_todigit({prefix}codepoint character) {{\n')
        file.write(f'    return {prefix}getcodepointdata(character)->numeric_value;\n')
        file.write('}\n\n')

        file.write(f'long {prefix}codepoint_toflags({prefix}codepoint character) {{\n')
        file.write(f'    return {prefix}getcodepointdata(character)->flags;\n')
        file.write('}\n\n')

        file.write(f'int {prefix}codepoint_islower({prefix}codepoint character) {{\n')
        file.write(f'    return !!({prefix}getcodepointdata(character)->flags & {prefix_upper}CODEPOINT_LOWER);\n')
        file.write('}\n\n')

        file.write(f'int {prefix}codepoint_isupper({prefix}codepoint character) {{\n')
        file.write(f'    return !!({prefix}getcodepointdata(character)->flags & {prefix_upper}CODEPOINT_UPPER);\n')
        file.write('}\n\n')

        file.write(f'int {prefix}codepoint_istitle({prefix}codepoint character) {{\n')
        file.write(f'    return !!({prefix}getcodepointdata(character)->flags & {prefix_upper}CODEPOINT_TITLE);\n')
        file.write('}\n\n')

        file.write(f'int {prefix}codepoint_isdigit({prefix}codepoint character) {{\n')
        file.write(f'    return !!({prefix}getcodepointdata(character)->flags & {prefix_upper}CODEPOINT_DIGIT);\n')
        file.write('}\n\n')

        file.write(f'int {prefix}codepoint_isspace({prefix}codepoint character) {{\n')
        file.write(f'    return !!({prefix}getcodepointdata(character)->flags & {prefix_upper}CODEPOINT_SPACE);\n')
        file.write('}\n\n')

        file.write(f'int {prefix}codepoint_ispunct({prefix}codepoint character) {{\n')
        file.write(f'    return !!({prefix}getcodepointdata(character)->flags & {prefix_upper}CODEPOINT_PUNCTUATION);\n')
        file.write('}\n\n')

        file.write(f'int {prefix}codepoint_isprint({prefix}codepoint character) {{\n')
        file.write(f'    return !!({prefix}getcodepointdata(character)->flags & {prefix_upper}CODEPOINT_PRINTABLE);\n')
        file.write('}\n\n')

        file.write(f'int {prefix}codepoint_iscntrl({prefix}codepoint character) {{\n')
        file.write(f'    return !!({prefix}getcodepointdata(character)->flags & {prefix_upper}CODEPOINT_CONTROL);\n')
        file.write('}\n\n')

        file.write(f'int {prefix}codepoint_isemoji({prefix}codepoint character) {{\n')
        file.write(f'    return !!({prefix}getcodepointdata(character)->flags & {prefix_upper}CODEPOINT_EMOJI);\n')
        file.write('}\n\n')

        file.write(f'int {prefix}codepoint_isalpha({prefix}codepoint character) {{\n')
        file.write(f'    return !!({prefix}getcodepointdata(character)->flags & {prefix_upper}CODEPOINT_ALPHA);\n')
        file.write('}\n\n')

        file.write(f'int {prefix}codepoint_isalnum({prefix}codepoint character) {{\n')
        file.write(f'    return !!({prefix}getcodepointdata(character)->flags & ({prefix_upper}CODEPOINT_ALPHA | {prefix_upper}CODEPOINT_DIGIT));\n')
        file.write('}\n\n')

        file.write(f'int {prefix}codepoint_isvalid({prefix}codepoint character) {{\n')
        file.write(f'    return {prefix}getcodepointdata(character) != &unicode_codepoints[0];\n')
        file.write('}\n\n')

        file.write('#endif\n')  # end of implementation
        file.write('\n')

if __name__ == "__main__":
    # This script relies on Python 3.6's ordred dictionary feature.
    # Prior versions of python did not order dictionary entries.
    if sys.version_info[0] < 3 or sys.version_info[1] < 6:
        raise Exception("This script required Python 3.6 or newer")
    main()
