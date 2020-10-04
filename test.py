#!/usr/bin/env python3

#  test.py - Verifies the generated Unicode code point data is correct.
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

import unittest
import subprocess
import os
import sys
import json

class TestUnicodeUtility(unittest.TestCase):
    # Verify the usage instructions are printed when no argument is given.
    def test_no_arguments(self):
        output, exit_code = self.execute_compiler([])
        self.assertEqual(output, "usage: unicode [--json] codepoint\n")
        self.assertEqual(exit_code, 1)

    # 'LOW LINE' (U+005F)
    # Test a code point that indicates a connecting character.
    def test_underscore(self):
        output, exit_code = self.execute_compiler(["--json", "U+005F"])
        output = json.loads(output)
        self.assertEqual(output['toLowerCase'], 95)
        self.assertEqual(output['toUpperCase'], 95)
        self.assertEqual(output['toTitleCase'], 95)
        self.assertEqual(output['toDigit'], 0)
        self.assertEqual(output['isLowerCase'], 0)
        self.assertEqual(output['isUpperCase'], 0)
        self.assertEqual(output['isTitleCase'], 0)
        self.assertEqual(output['isDigit'], 0)
        self.assertEqual(output['isSpaceChar'], 0)
        self.assertEqual(output['isLineBreak'], 0)
        self.assertEqual(output['isISOControl'], 0)
        self.assertEqual(output['isPunctuation'], 1)
        self.assertEqual(output['isConnectingChar'], 1)
        self.assertEqual(output['isFormattingChar'], 0)
        self.assertEqual(output['isCombiningChar'], 0)
        self.assertEqual(output['isEmoji'], 0)
        self.assertEqual(output['isPrintable'], 1)
        self.assertEqual(output['isAlpha'], 0)
        self.assertEqual(output['isAlphaNumeric'], 0)
        self.assertEqual(output['isValidCodePoint'], 1)
        self.assertEqual(exit_code, 0)

    # 'LINE SEPARATOR' (U+2028)
    # Test a code point that indicates a line break.
    def test_line_separator(self):
        output, exit_code = self.execute_compiler(["--json", "U+2028"])
        output = json.loads(output)
        self.assertEqual(output['toLowerCase'], 8232)
        self.assertEqual(output['toUpperCase'], 8232)
        self.assertEqual(output['toTitleCase'], 8232)
        self.assertEqual(output['toDigit'], 0)
        self.assertEqual(output['isLowerCase'], 0)
        self.assertEqual(output['isUpperCase'], 0)
        self.assertEqual(output['isTitleCase'], 0)
        self.assertEqual(output['isDigit'], 0)
        self.assertEqual(output['isSpaceChar'], 0)
        self.assertEqual(output['isLineBreak'], 1)
        self.assertEqual(output['isISOControl'], 0)
        self.assertEqual(output['isPunctuation'], 0)
        self.assertEqual(output['isConnectingChar'], 0)
        self.assertEqual(output['isFormattingChar'], 0)
        self.assertEqual(output['isCombiningChar'], 0)
        self.assertEqual(output['isEmoji'], 0)
        self.assertEqual(output['isPrintable'], 0)
        self.assertEqual(output['isAlpha'], 0)
        self.assertEqual(output['isAlphaNumeric'], 0)
        self.assertEqual(output['isValidCodePoint'], 1)
        self.assertEqual(exit_code, 0)

    # 'LATIN CAPITAL LETTER Z' (U+005A)
    # Test a code point with a lower and upper case, but not a title case.
    def test_latin_capital_letter_Z(self):
        output, exit_code = self.execute_compiler(["--json", "U+005A"])
        output = json.loads(output)
        self.assertEqual(output['toLowerCase'], 122)
        self.assertEqual(output['toUpperCase'], 90)
        self.assertEqual(output['toTitleCase'], 90)
        self.assertEqual(output['toDigit'], 0)
        self.assertEqual(output['isLowerCase'], 0)
        self.assertEqual(output['isUpperCase'], 1)
        self.assertEqual(output['isTitleCase'], 0)
        self.assertEqual(output['isDigit'], 0)
        self.assertEqual(output['isSpaceChar'], 0)
        self.assertEqual(output['isLineBreak'], 0)
        self.assertEqual(output['isISOControl'], 0)
        self.assertEqual(output['isPunctuation'], 0)
        self.assertEqual(output['isConnectingChar'], 0)
        self.assertEqual(output['isFormattingChar'], 0)
        self.assertEqual(output['isCombiningChar'], 0)
        self.assertEqual(output['isEmoji'], 0)
        self.assertEqual(output['isPrintable'], 1)
        self.assertEqual(output['isAlpha'], 1)
        self.assertEqual(output['isAlphaNumeric'], 1)
        self.assertEqual(output['isValidCodePoint'], 1)
        self.assertEqual(exit_code, 0)

    # 'TIBETAN MARK BSKA- SHOG GI MGO RGYAN' (U+0FD0)
    # Test a punctuation character.
    def test_tibetan_mark_bska_shog_gi_mgo_rgyan(self):
        output, exit_code = self.execute_compiler(["--json", "U+0FD0"])
        output = json.loads(output)
        self.assertEqual(output['toLowerCase'], 4048)
        self.assertEqual(output['toUpperCase'], 4048)
        self.assertEqual(output['toTitleCase'], 4048)
        self.assertEqual(output['toDigit'], 0)
        self.assertEqual(output['isLowerCase'], 0)
        self.assertEqual(output['isUpperCase'], 0)
        self.assertEqual(output['isTitleCase'], 0)
        self.assertEqual(output['isDigit'], 0)
        self.assertEqual(output['isSpaceChar'], 0)
        self.assertEqual(output['isLineBreak'], 0)
        self.assertEqual(output['isISOControl'], 0)
        self.assertEqual(output['isPunctuation'], 1)
        self.assertEqual(output['isConnectingChar'], 0)
        self.assertEqual(output['isFormattingChar'], 0)
        self.assertEqual(output['isCombiningChar'], 0)
        self.assertEqual(output['isEmoji'], 0)
        self.assertEqual(output['isPrintable'], 1)
        self.assertEqual(output['isAlpha'], 0)
        self.assertEqual(output['isAlphaNumeric'], 0)
        self.assertEqual(output['isValidCodePoint'], 1)
        self.assertEqual(exit_code, 0)

    # 'NARROW NO-BREAK SPACE' (U+202F)
    # Test a space character.
    def test_narrow_no_break_space(self):
        output, exit_code = self.execute_compiler(["--json", "U+202F"])
        output = json.loads(output)
        self.assertEqual(output['toLowerCase'], 8239)
        self.assertEqual(output['toUpperCase'], 8239)
        self.assertEqual(output['toTitleCase'], 8239)
        self.assertEqual(output['toDigit'], 0)
        self.assertEqual(output['isLowerCase'], 0)
        self.assertEqual(output['isUpperCase'], 0)
        self.assertEqual(output['isTitleCase'], 0)
        self.assertEqual(output['isDigit'], 0)
        self.assertEqual(output['isSpaceChar'], 1)
        self.assertEqual(output['isLineBreak'], 0)
        self.assertEqual(output['isISOControl'], 0)
        self.assertEqual(output['isPunctuation'], 0)
        self.assertEqual(output['isConnectingChar'], 0)
        self.assertEqual(output['isFormattingChar'], 0)
        self.assertEqual(output['isCombiningChar'], 0)
        self.assertEqual(output['isEmoji'], 0)
        self.assertEqual(output['isPrintable'], 0)
        self.assertEqual(output['isAlpha'], 0)
        self.assertEqual(output['isAlphaNumeric'], 0)
        self.assertEqual(output['isValidCodePoint'], 1)
        self.assertEqual(exit_code, 0)

    # 'SPACE' (U+0020)
    # Test a space character that's considered printable.
    def test_space(self):
        output, exit_code = self.execute_compiler(["--json", "U+0020"])
        output = json.loads(output)
        self.assertEqual(output['toLowerCase'], 32)
        self.assertEqual(output['toUpperCase'], 32)
        self.assertEqual(output['toTitleCase'], 32)
        self.assertEqual(output['toDigit'], 0)
        self.assertEqual(output['isLowerCase'], 0)
        self.assertEqual(output['isUpperCase'], 0)
        self.assertEqual(output['isTitleCase'], 0)
        self.assertEqual(output['isDigit'], 0)
        self.assertEqual(output['isSpaceChar'], 1)
        self.assertEqual(output['isLineBreak'], 0)
        self.assertEqual(output['isISOControl'], 0)
        self.assertEqual(output['isPunctuation'], 0)
        self.assertEqual(output['isConnectingChar'], 0)
        self.assertEqual(output['isFormattingChar'], 0)
        self.assertEqual(output['isCombiningChar'], 0)
        self.assertEqual(output['isEmoji'], 0)
        self.assertEqual(output['isPrintable'], 1)
        self.assertEqual(output['isAlpha'], 0)
        self.assertEqual(output['isAlphaNumeric'], 0)
        self.assertEqual(output['isValidCodePoint'], 1)
        self.assertEqual(exit_code, 0)

    # 'SYNCHRONOUS IDLE' (U+0016)
    # Test a control character.
    def test_synchronous_idle(self):
        output, exit_code = self.execute_compiler(["--json", "U+0016"])
        output = json.loads(output)
        self.assertEqual(output['toLowerCase'], 22)
        self.assertEqual(output['toUpperCase'], 22)
        self.assertEqual(output['toTitleCase'], 22)
        self.assertEqual(output['toDigit'], 0)
        self.assertEqual(output['isLowerCase'], 0)
        self.assertEqual(output['isUpperCase'], 0)
        self.assertEqual(output['isTitleCase'], 0)
        self.assertEqual(output['isDigit'], 0)
        self.assertEqual(output['isSpaceChar'], 0)
        self.assertEqual(output['isLineBreak'], 0)
        self.assertEqual(output['isISOControl'], 1)
        self.assertEqual(output['isPunctuation'], 0)
        self.assertEqual(output['isConnectingChar'], 0)
        self.assertEqual(output['isFormattingChar'], 0)
        self.assertEqual(output['isCombiningChar'], 0)
        self.assertEqual(output['isEmoji'], 0)
        self.assertEqual(output['isPrintable'], 0)
        self.assertEqual(output['isAlpha'], 0)
        self.assertEqual(output['isAlphaNumeric'], 0)
        self.assertEqual(output['isValidCodePoint'], 1)
        self.assertEqual(exit_code, 0)

    # 'HANGUL SYLLABLE HIK' (U+D7A0)
    # Test a code point generated from a range of code points.
    def test_hangul_syllable_hik(self):
        output, exit_code = self.execute_compiler(["--json", "U+D7A0"])
        output = json.loads(output)
        self.assertEqual(output['toLowerCase'], 55200)
        self.assertEqual(output['toUpperCase'], 55200)
        self.assertEqual(output['toTitleCase'], 55200)
        self.assertEqual(output['toDigit'], 0)
        self.assertEqual(output['isLowerCase'], 0)
        self.assertEqual(output['isUpperCase'], 0)
        self.assertEqual(output['isTitleCase'], 0)
        self.assertEqual(output['isDigit'], 0)
        self.assertEqual(output['isSpaceChar'], 0)
        self.assertEqual(output['isLineBreak'], 0)
        self.assertEqual(output['isISOControl'], 0)
        self.assertEqual(output['isPunctuation'], 0)
        self.assertEqual(output['isConnectingChar'], 0)
        self.assertEqual(output['isFormattingChar'], 0)
        self.assertEqual(output['isCombiningChar'], 0)
        self.assertEqual(output['isEmoji'], 0)
        self.assertEqual(output['isPrintable'], 1)
        self.assertEqual(output['isAlpha'], 1)
        self.assertEqual(output['isAlphaNumeric'], 1)
        self.assertEqual(output['isValidCodePoint'], 1)
        self.assertEqual(exit_code, 0)

    # 'ARABIC-INDIC DIGIT SEVEN' (U+0667)
    # Test a code point that's a digit.
    def test_arabic_indic_digit_seven(self):
        output, exit_code = self.execute_compiler(["--json", "U+0667"])
        output = json.loads(output)
        self.assertEqual(output['toLowerCase'], 1639)
        self.assertEqual(output['toUpperCase'], 1639)
        self.assertEqual(output['toTitleCase'], 1639)
        self.assertEqual(output['toDigit'], 7)
        self.assertEqual(output['isLowerCase'], 0)
        self.assertEqual(output['isUpperCase'], 0)
        self.assertEqual(output['isTitleCase'], 0)
        self.assertEqual(output['isDigit'], 1)
        self.assertEqual(output['isSpaceChar'], 0)
        self.assertEqual(output['isLineBreak'], 0)
        self.assertEqual(output['isISOControl'], 0)
        self.assertEqual(output['isPunctuation'], 0)
        self.assertEqual(output['isConnectingChar'], 0)
        self.assertEqual(output['isFormattingChar'], 0)
        self.assertEqual(output['isCombiningChar'], 0)
        self.assertEqual(output['isEmoji'], 0)
        self.assertEqual(output['isPrintable'], 1)
        self.assertEqual(output['isAlpha'], 0)
        self.assertEqual(output['isAlphaNumeric'], 1)
        self.assertEqual(output['isValidCodePoint'], 1)
        self.assertEqual(exit_code, 0)


    # 'SUPERSCRIPT THREE' (U+00B3)
    # Test a code point with a digit representation, but that's not a digit.
    def test_superscript_one(self):
        output, exit_code = self.execute_compiler(["--json", "U+00B3"])
        output = json.loads(output)
        self.assertEqual(output['toLowerCase'], 179)
        self.assertEqual(output['toUpperCase'], 179)
        self.assertEqual(output['toTitleCase'], 179)
        self.assertEqual(output['toDigit'], 3)
        self.assertEqual(output['isLowerCase'], 0)
        self.assertEqual(output['isUpperCase'], 0)
        self.assertEqual(output['isTitleCase'], 0)
        self.assertEqual(output['isDigit'], 0)
        self.assertEqual(output['isSpaceChar'], 0)
        self.assertEqual(output['isLineBreak'], 0)
        self.assertEqual(output['isISOControl'], 0)
        self.assertEqual(output['isPunctuation'], 0)
        self.assertEqual(output['isConnectingChar'], 0)
        self.assertEqual(output['isFormattingChar'], 0)
        self.assertEqual(output['isCombiningChar'], 0)
        self.assertEqual(output['isEmoji'], 0)
        self.assertEqual(output['isPrintable'], 1)
        self.assertEqual(output['isAlpha'], 0)
        self.assertEqual(output['isAlphaNumeric'], 0)
        self.assertEqual(output['isValidCodePoint'], 1)
        self.assertEqual(exit_code, 0)

    # 'LATIN CAPITAL LETTER DZ WITH CARON' (U+01C4)
    # Test a upper case code point with a unique lower case and title case.
    def test_latin_capital_letter_DZ_with_caron(self):
        output, exit_code = self.execute_compiler(["--json", "U+01C4"])
        output = json.loads(output)
        self.assertEqual(output['toLowerCase'], 454)
        self.assertEqual(output['toUpperCase'], 452)
        self.assertEqual(output['toTitleCase'], 453)
        self.assertEqual(output['toDigit'], 0)
        self.assertEqual(output['isLowerCase'], 0)
        self.assertEqual(output['isUpperCase'], 1)
        self.assertEqual(output['isTitleCase'], 0)
        self.assertEqual(output['isDigit'], 0)
        self.assertEqual(output['isSpaceChar'], 0)
        self.assertEqual(output['isLineBreak'], 0)
        self.assertEqual(output['isISOControl'], 0)
        self.assertEqual(output['isPunctuation'], 0)
        self.assertEqual(output['isConnectingChar'], 0)
        self.assertEqual(output['isFormattingChar'], 0)
        self.assertEqual(output['isCombiningChar'], 0)
        self.assertEqual(output['isEmoji'], 0)
        self.assertEqual(output['isPrintable'], 1)
        self.assertEqual(output['isAlpha'], 1)
        self.assertEqual(output['isAlphaNumeric'], 1)
        self.assertEqual(output['isValidCodePoint'], 1)
        self.assertEqual(exit_code, 0)

    # 'LATIN CAPITAL LETTER D WITH SMALL LETTER Z WITH CARON' (U+01C5)
    # Test a title case code point with a unique lower case and upper case.
    def test_latin_capital_letter_D_with_small_letter_Z_with_caron(self):
        output, exit_code = self.execute_compiler(["--json", "U+01C5"])
        output = json.loads(output)
        self.assertEqual(output['toLowerCase'], 454)
        self.assertEqual(output['toUpperCase'], 452)
        self.assertEqual(output['toTitleCase'], 453)
        self.assertEqual(output['toDigit'], 0)
        self.assertEqual(output['isLowerCase'], 0)
        self.assertEqual(output['isUpperCase'], 0)
        self.assertEqual(output['isTitleCase'], 1)
        self.assertEqual(output['isDigit'], 0)
        self.assertEqual(output['isSpaceChar'], 0)
        self.assertEqual(output['isLineBreak'], 0)
        self.assertEqual(output['isISOControl'], 0)
        self.assertEqual(output['isPunctuation'], 0)
        self.assertEqual(output['isConnectingChar'], 0)
        self.assertEqual(output['isFormattingChar'], 0)
        self.assertEqual(output['isCombiningChar'], 0)
        self.assertEqual(output['isEmoji'], 0)
        self.assertEqual(output['isPrintable'], 1)
        self.assertEqual(output['isAlpha'], 1)
        self.assertEqual(output['isAlphaNumeric'], 1)
        self.assertEqual(output['isValidCodePoint'], 1)
        self.assertEqual(exit_code, 0)

    # 'LATIN SMALL LETTER DZ WITH CARON' (U+01C6)
    # Test a lower case code point with a unique upper case and title case.
    def test_latin_small_letter_DZ_with_caron(self):
        output, exit_code = self.execute_compiler(["--json", "U+01C6"])
        output = json.loads(output)
        self.assertEqual(output['toLowerCase'], 454)
        self.assertEqual(output['toUpperCase'], 452)
        self.assertEqual(output['toTitleCase'], 453)
        self.assertEqual(output['toDigit'], 0)
        self.assertEqual(output['isLowerCase'], 1)
        self.assertEqual(output['isUpperCase'], 0)
        self.assertEqual(output['isTitleCase'], 0)
        self.assertEqual(output['isDigit'], 0)
        self.assertEqual(output['isSpaceChar'], 0)
        self.assertEqual(output['isLineBreak'], 0)
        self.assertEqual(output['isISOControl'], 0)
        self.assertEqual(output['isPunctuation'], 0)
        self.assertEqual(output['isConnectingChar'], 0)
        self.assertEqual(output['isFormattingChar'], 0)
        self.assertEqual(output['isCombiningChar'], 0)
        self.assertEqual(output['isEmoji'], 0)
        self.assertEqual(output['isPrintable'], 1)
        self.assertEqual(output['isAlpha'], 1)
        self.assertEqual(output['isAlphaNumeric'], 1)
        self.assertEqual(output['isValidCodePoint'], 1)
        self.assertEqual(exit_code, 0)

    # 'PILE OF POO' (U+1F4A9)
    # Test an Emoji.
    def test_pile_of_poo(self):
        output, exit_code = self.execute_compiler(["--json", "U+1F4A9"])
        output = json.loads(output)
        self.assertEqual(output['toLowerCase'], 128169)
        self.assertEqual(output['toUpperCase'], 128169)
        self.assertEqual(output['toTitleCase'], 128169)
        self.assertEqual(output['toDigit'], 0)
        self.assertEqual(output['isLowerCase'], 0)
        self.assertEqual(output['isUpperCase'], 0)
        self.assertEqual(output['isTitleCase'], 0)
        self.assertEqual(output['isDigit'], 0)
        self.assertEqual(output['isSpaceChar'], 0)
        self.assertEqual(output['isLineBreak'], 0)
        self.assertEqual(output['isISOControl'], 0)
        self.assertEqual(output['isPunctuation'], 0)
        self.assertEqual(output['isConnectingChar'], 0)
        self.assertEqual(output['isFormattingChar'], 0)
        self.assertEqual(output['isCombiningChar'], 0)
        self.assertEqual(output['isEmoji'], 1)
        self.assertEqual(output['isPrintable'], 1)
        self.assertEqual(output['isAlpha'], 0)
        self.assertEqual(output['isAlphaNumeric'], 0)
        self.assertEqual(output['isValidCodePoint'], 1)
        self.assertEqual(exit_code, 0)

    # Test an invalid code point (U+F4F1)
    def test_invalid_character(self):
        output, exit_code = self.execute_compiler(["--json", "U+F4F1"])
        output = json.loads(output)
        self.assertEqual(output['toLowerCase'], 62705)
        self.assertEqual(output['toUpperCase'], 62705)
        self.assertEqual(output['toTitleCase'], 62705)
        self.assertEqual(output['toDigit'], 0)
        self.assertEqual(output['isLowerCase'], 0)
        self.assertEqual(output['isUpperCase'], 0)
        self.assertEqual(output['isTitleCase'], 0)
        self.assertEqual(output['isDigit'], 0)
        self.assertEqual(output['isSpaceChar'], 0)
        self.assertEqual(output['isLineBreak'], 0)
        self.assertEqual(output['isISOControl'], 0)
        self.assertEqual(output['isPunctuation'], 0)
        self.assertEqual(output['isConnectingChar'], 0)
        self.assertEqual(output['isFormattingChar'], 0)
        self.assertEqual(output['isCombiningChar'], 0)
        self.assertEqual(output['isEmoji'], 0)
        self.assertEqual(output['isPrintable'], 0)
        self.assertEqual(output['isAlpha'], 0)
        self.assertEqual(output['isAlphaNumeric'], 0)
        self.assertEqual(output['isValidCodePoint'], 0)
        self.assertEqual(exit_code, 0)

    # --------------------------------------------------------------------------------
    #
    # Test Helpers go below this point.
    # Unit tests go above this point.
    #
    # --------------------------------------------------------------------------------

    # A helper method to execute the unicode utility.
    # This is used by tests, but is not a test itself.
    def execute_compiler(self, options = []):
        if not os.path.exists("example"):
            print("executable missing; be sure to run 'make' before running tests")
            sys.exit(1)
        process = subprocess.Popen(["./example"] + options, stdout=subprocess.PIPE)
        output, error = process.communicate()
        exit_code = process.wait()
        return (output.decode("ascii"), exit_code)

if __name__ == "__main__":
    unittest.main()
