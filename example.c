/*
 *  libcodepoint.py - Generates a C file with a Unicode lookup table.
 *  Copyright (c) 2020 Henry G. Stratmann III
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#define CODEPOINT_IMPLEMENTATION
#include "codepoints.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

static void print_usage_and_quit(void)
{
    puts("usage: unicode [--json] codepoint");
    exit(1);
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        print_usage_and_quit();
    }

    int codepoint_argument_index = -1; // Assume the user fails to pass a code point until proven otherwise.
    bool output_json = false; // Assume textual output until asked to emit JSON.

    for (int i = 1; i < argc; i++)
    {
        if (argv[i][0] == '-') // Check for an option.
        {
            // Check what kind of option was supplied.
            if (strcmp(argv[i], "--json") == 0)
            {
                output_json = true;
            }
        }
        else
        {
            // Since this isn't an option, assume it's a Unicode code point.
            codepoint_argument_index = i;
        }
    }

    // If no code point was supplied, then exit.
    if (codepoint_argument_index < 0)
    {
        print_usage_and_quit();
    }

    const char *unicode_codepoint = argv[codepoint_argument_index];

    // If the code point is written in "U+" notation, then advance
    // past the 'U' and '+' so only the hexadecimal digits remain.
    if (tolower(*unicode_codepoint) == 'u')
    {
        unicode_codepoint += 1; // advance past the 'u'
        if (*unicode_codepoint == '+')
        {
            unicode_codepoint += 1; // advance past the '+'
        }
    }

    // Convert the code point from a string to its hexadecimal value,
    // then serialize out its attributes.
    const codepoint character = strtol(unicode_codepoint, NULL, 16);

    if (output_json)
    {
        putchar('{');
        printf("\"toLowerCase\":%d,", codepoint_tolower(character));
        printf("\"toUpperCase\":%d,", codepoint_toupper(character));
        printf("\"toTitleCase\":%d,", codepoint_totitle(character));
        printf("\"toDigit\":%d,", codepoint_todigit(character));
        printf("\"isLowerCase\":%s,", codepoint_islower(character) ? "true" : "false");
        printf("\"isUpperCase\":%s,", codepoint_isupper(character) ? "true" : "false");
        printf("\"isTitleCase\":%s,", codepoint_istitle(character) ? "true" : "false");
        printf("\"isDigit\":%s,", codepoint_isdigit(character) ? "true" : "false");
        printf("\"isSpaceChar\":%s,", codepoint_isspace(character) ? "true" : "false");
        printf("\"isLineBreak\":%s,", (codepoint_toflags(character) & CODEPOINT_LINEBREAK) ? "true" : "false");
        printf("\"isISOControl\":%s,", codepoint_iscntrl(character) ? "true" : "false");
        printf("\"isPunctuation\":%s,", codepoint_ispunct(character) ? "true" : "false");
        printf("\"isConnectingChar\":%s,", (codepoint_toflags(character) & CODEPOINT_CONNECTING) ? "true" : "false");
        printf("\"isFormattingChar\":%s,", (codepoint_toflags(character) & CODEPOINT_FORMATTING) ? "true" : "false");
        printf("\"isCombiningChar\":%s,", (codepoint_toflags(character) & CODEPOINT_COMBINING) ? "true" : "false");
        printf("\"isEmoji\":%s,", codepoint_isemoji(character) ? "true" : "false");
        printf("\"isPrintable\":%s,", codepoint_isprint(character) ? "true" : "false");
        printf("\"isAlpha\":%s,", codepoint_isalpha(character) ? "true" : "false");
        printf("\"isAlphaNumeric\":%s,", codepoint_isalnum(character) ? "true" : "false");
        printf("\"isValidCodePoint\":%s", codepoint_isvalid(character) ? "true" : "false");
        putchar('}');
    }
    else
    {
        printf("toLowerCase: %d\n", codepoint_tolower(character));
        printf("toUpperCase: %d\n", codepoint_toupper(character));
        printf("toTitleCase: %d\n", codepoint_totitle(character));
        printf("toDigit: %d\n", codepoint_todigit(character));
        printf("isLowerCase: %d\n", codepoint_islower(character));
        printf("isUpperCase: %d\n", codepoint_isupper(character));
        printf("isTitleCase: %d\n", codepoint_istitle(character));
        printf("isDigit: %d\n", codepoint_isdigit(character));
        printf("isSpaceChar: %d\n", codepoint_isspace(character));
        printf("isISOControl: %d\n", codepoint_iscntrl(character));
        printf("isPunctuation: %d\n", codepoint_ispunct(character));
        printf("isEmoji: %d\n", codepoint_isemoji(character));
        printf("isPrintable: %d\n", codepoint_isprint(character));
        printf("isAlpha: %d\n", codepoint_isalpha(character));
        printf("isAlphaNumeric: %d\n", codepoint_isalnum(character));
        printf("isValidCodePoint: %d\n", codepoint_isvalid(character));
    }

    return 0;
}
