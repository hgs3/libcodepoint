# Unicode Code Point Library

A single header library for transforming and querying information about Unicode code points.

This is **not** a string library. It operates exclusively on individual code points.
Character encoding, decoding, and all other string manipulation is the users responsibility.

## Features

* Single header file.
* Lightweight (all Unicode code points compressed to ~210kb).
* Optimized retrieval from a precalculated lookup table.
* Simple C API.
* No dependencies.

## Installation

The repo contains the scripts to generate the header. It does not contain the header itself.

You can download a prebuilt header from the releases page.

If your compiler does not provide the `stdint.h` header or the `inline` keyword, then you can generate a header without them by following the [build instructions](#Building).

## Example Usage

The following example demonstrates the complete API.

The naming convention and behavior of the API mirrors the functions defined in the [ctype.h header](https://en.wikipedia.org/wiki/C_character_classification#Overview_of_functions).

```cpp
// Define 'CODEPOINT_IMPLEMENTATION' before including the header in one of your source files.
#define CODEPOINT_IMPLEMENTATION
#include "codepoints.h"

int main(int argc, char *argv)
{
    if (argc < 2)
    {
        puts("please provide a unicode code point in hexidecimal");
        return 1;
    }

    const codepoint character = strtol(argv[1], 0, 16);

    // ---------------
    // Transformations
    // ---------------
    printf("toLowerCase: %d\n", codepoint_tolower(character));
    printf("toUpperCase: %d\n", codepoint_toupper(character));
    printf("toTitleCase: %d\n", codepoint_totitle(character));
    printf("toDigit: %d\n", codepoint_todigit(character));

    // -------
    // Queries
    // -------
    printf("isLowerCase: %d\n", codepoint_islower(character));
    printf("isUpperCase: %d\n", codepoint_isupper(character));
    printf("isTitleCase: %d\n", codepoint_istitle(character));
    printf("isDigit: %d\n", codepoint_isdigit(character));
    printf("isSpaceChar: %d\n", codepoint_isspace(character));
    printf("isLineBreak: %d\n", codepoint_islnbrk(character));
    printf("isISOControl: %d\n", codepoint_iscntrl(character));
    printf("isPunctuation: %d\n", codepoint_ispunct(character));
    printf("isEmoji: %d\n", codepoint_isemoji(character));
    printf("isPrintable: %d\n", codepoint_isprint(character));
    printf("isLetter: %d\n", codepoint_isalpha(character));
    printf("isLetterOrDigit: %d\n", codepoint_isalnum(character));
    printf("isValidCodePoint: %d\n", codepoint_isvalid(character));
    return 0;
}
```

## Building

The `libcodepoint.py` script downloads the Unicode Consortium's code point database and generates a header file with all unicode code points compressed into a precalculated lookup table.

The header output is configurable. You can view all options by executing `libcodepoint.py` with `-h` or `--help`.

For example, the usage of the `inline` keyword and `stdint.h` header can be suppressed with:

```
$ libcodepoint.py --no-stdint --no-inline codepoints.h
```

## License

All source code in this repository is licensed under the [Affero GPLv3](LICENSE).

The GPL does not apply to program input or output therefore you can choose your own license for the generated header.
