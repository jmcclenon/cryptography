from collections import Counter
import argparse, base64

# ENGLISH_LETTERS_FREQUENCY = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99,
#                      'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
#                      'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
#
# LETTERS_SORTED_BY_POPULARITY = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
# LETTERS_SORTED_ALPHABETICALLY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# LETTERS_DICTIONARY = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0,
#                 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0,
#                 'Y': 0, 'Z': 0}
#
#
# def do_print_frequency(pDictionary, pTotalCount):
#
#     TWO_DECIMAL_PLACES = "{0:.2f}"
#     lFrequencyPercent = 0
#
#     print()
#     for letter, frequency in pDictionary.items():
#         lFrequencyPercent = frequency / pTotalCount * 100
#         lBestMatch = ''
#         lBestFrequencyMatch = 100.0
#         lCurrentDifference = 100.00
#         lSmallestDifference = 100.00
#         for englishLetter, englishLetterFrequency in ENGLISH_LETTERS_FREQUENCY.items():
#             lCurrentDifference = abs(lFrequencyPercent - englishLetterFrequency)
#             if lCurrentDifference < lSmallestDifference:
#                 lBestMatch = englishLetter
#                 lBestFrequencyMatch = englishLetterFrequency
#                 lSmallestDifference = lCurrentDifference
#             #end if
#         #end for
#         lFrequencyPercentString = TWO_DECIMAL_PLACES.format(lFrequencyPercent)
#         lBestFrequencyMatchString = 'Best Match: ' + lBestMatch + '(' + TWO_DECIMAL_PLACES.format(lBestFrequencyMatch) + ')'
#         print(letter, frequency, lFrequencyPercentString, lBestFrequencyMatchString)
#
#
# def do_print_histogram(pDictionary, pTotalCount):
#
#     lFrequencyBarLength = 0
#
#     print()
#     for letter, frequency in pDictionary.items():
#         lFrequencyBarLength = int(frequency / pTotalCount * 500)
#         print(letter, frequency, "#" * lFrequencyBarLength)
#
# def do_analysis(pTextLine):
#
#     lTotalCount = 0
#
#     for character in pTextLine.upper():
#         if character in LETTERS_SORTED_ALPHABETICALLY:
#             LETTERS_DICTIONARY[character]+=1
#             lTotalCount+=1
#
#     do_print_frequency(LETTERS_DICTIONARY, lTotalCount)
#     do_print_histogram(LETTERS_DICTIONARY, lTotalCount)
#
#
# def do_analysis(pTextFile):
#
#     lTotalCount = 0
#
#     for line in pTextFile:
#         for character in line.upper():
#             if character in LETTERS_SORTED_ALPHABETICALLY:
#                 LETTERS_DICTIONARY[character]+=1
#                 lTotalCount+=1
#
#     do_print_frequency(LETTERS_DICTIONARY, lTotalCount)
#     do_print_histogram(LETTERS_DICTIONARY, lTotalCount)


def do_print_histogram(pByteCounts: dict, pTotalBytes: int, pShowHistogram: bool, pShowASCII: bool, pShowByteCount: bool, pVerbose: bool) -> None:

    lScaleFactor = 5
    lFrequencyBarLength = 0
    lOutput = ''

    for lByte, lByteCount in pByteCounts.items():
        lFrequencyBarLength = int(lByteCount / pTotalBytes * 100 * lScaleFactor)

        lOutput = ''
        if pVerbose: lOutput = 'Byte: '
        lOutput += str(lByte) + ' '
        if pShowASCII: lOutput += chr(lByte) + ' '
        if pShowByteCount: lOutput += str(lByteCount) + ' '
        if pShowHistogram: lOutput += "#" * lFrequencyBarLength
        print(lOutput)

def analyze(pInput: bytearray, pShowHistogram: bool, pShowASCII: bool, pShowByteCount: bool, pVerbose: bool) -> None:
    lByteCounts = dict.fromkeys(range(0,256), 0)
    lTotalBytes = 0

    for lByte in pInput:
        lByteCounts[lByte] +=1
        lTotalBytes += 1

    do_print_histogram(lByteCounts, lTotalBytes, pShowHistogram, pShowASCII, pShowByteCount, pVerbose)


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser()
    lArgParser.add_argument('-g', '--show-histogram', help='Show histogram for each byte of input', action='store_true')
    lArgParser.add_argument('-s', '--show-ascii', help='Show ascii representation for each byte of input', action='store_true')
    lArgParser.add_argument('-c', '--show-byte-count', help='Show count for each byte of input', action='store_true')
    lArgParser.add_argument('-a', '--show-all', help='Show count, ascii represenation and histogram for each byte of input. Equivalent to -gsc', action='store_true')
    lArgParser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lArgParser.add_argument('-if', '--input-format', help='Input format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store')
    lArgParser.add_argument('-i', '--input-file', help='Read INPUT from an input file', action='store')
    lArgParser.add_argument('INPUT', nargs='?', help='INPUT to analyze', type=str, action='store')
    lArgs = lArgParser.parse_args()

    if lArgs.input_file:
        if lArgs.input_format == 'base64':
            with open(lArgs.input_file, 'rb') as lFile:
                lInput = bytearray(base64.b64decode(lFile.read()))
        else:
            with open(lArgs.input_file, 'rb') as lFile:
                lInput = bytearray(lFile.read())
    else:
        if lArgs.input_format == 'character':
            lInput = bytearray(lArgs.INPUT.encode())
        elif lArgs.input_format == 'base64':
            lInput = bytearray(base64.b64decode(lArgs.INPUT))
        elif lArgs.input_format == 'binary':
            lInput = bytearray(lArgs.INPUT)

    if lArgs.show_all: lArgs.show_histogram = lArgs.show_ascii = lArgs.show_byte_count = True

    analyze(lInput, lArgs.show_histogram, lArgs.show_ascii, lArgs.show_byte_count, lArgs.verbose)
