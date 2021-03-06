import argparse, base64, math
from argparse import RawTextHelpFormatter


TWO_DECIMAL_PLACES = "{0:.2f}"
MODULUS = 256


def get_byte_counts(pInput: bytearray) -> tuple:

    lByteCounts = dict.fromkeys(range(0,256), 0)
    lTotalBytes = 0

    for lByte in pInput:
        lByteCounts[lByte] += 1
        lTotalBytes += 1
    # end for

    return lByteCounts, lTotalBytes


def get_statistics(pInput: bytearray) -> tuple:
    # Mean = Average = SUM FROM 0 to N-1 / N
    # Median = (N / 2)th value after sorting values
    # Mode = Winner of popularity contest
    # Variance = SUM FROM 0 to N-1[(i - Mean)**2] / N
    # Standard Deviation = SquareRoot(Variance)

    lByteCounts = dict.fromkeys(range(0,256), 0)
    lSum = 0
    lList = []
    lSumOfDifferencesSquared = 0.0

    for lByte in pInput:
        lByteCounts[lByte] += 1
        lSum += lByte
        lList.append(lByte)
    # end for

    lTotalBytes = len(lList)
    lMean = lSum / lTotalBytes
    lMedianPosition = math.ceil(lTotalBytes / 2)
    lList.sort()

    # if even number of elements, median (middle value) is considered the average of the two central elements
    # if odd number of elements, median is the central element
    if (lTotalBytes % 2) == 0:
        lMedian = (lList[lMedianPosition] + lList[lMedianPosition] + 1) / 2
    else:
        lMedian = lList[lMedianPosition]

    lMostPopularByte = -1
    lLeastPopularByte = -1
    lLargestCountOfBytes = 0
    lSmallestCountOfBytes = 2**64
    for lTuple in lByteCounts.items():
        if lTuple[1] > lLargestCountOfBytes:
            lLargestCountOfBytes = lTuple[1]
            lMostPopularByte = lTuple[0]
        # end if
        if lTuple[1] < lSmallestCountOfBytes:
            lSmallestCountOfBytes = lTuple[1]
            lLeastPopularByte = lTuple[0]
        # end if
    # end if

    lMode = lMostPopularByte
    lAntiMode = lLeastPopularByte
    lModeCount = lLargestCountOfBytes
    lAntiModeCount = lSmallestCountOfBytes

    # If the distribution were perfectly even, what would be the mode? How far off is the actual mode?
    lHomogonousModeCount = lTotalBytes / MODULUS
    lModeCountRatio = lModeCount / lHomogonousModeCount
    lAntiModeCountRatio = lAntiModeCount / lHomogonousModeCount

    for lInt in lList:
        lSumOfDifferencesSquared += (lInt - lMean)**2

    lVariance = lSumOfDifferencesSquared / lTotalBytes

    lStandardDeviation = math.sqrt(lVariance)

    return lMean, lMedian, lMode, lModeCount, lModeCountRatio, lAntiMode, lAntiModeCount, lAntiModeCountRatio, lVariance, lStandardDeviation


def get_entropy(pByteCounts: dict, pTotalBytes: int) -> float:
    # Shannon's Entropy -SUM FROM 0 to N-1(Pr[i] * LogBase2(Pr[i])) where
    # Pr[i] is the probability of element i occurring
    BASE2 = 2
    lEntropy = 0
    for lByte, lByteCount in pByteCounts.items():
        lProbabilityOfByte = lByteCount / pTotalBytes
        if lProbabilityOfByte > 0:
            lEntropy += -1 * lProbabilityOfByte * math.log(lProbabilityOfByte, BASE2)
    return lEntropy


def get_kappa_index_of_coincidence(pInput: bytearray) -> dict:
    # IOC:
    # For each shift, add up the times the two bytes offset by lBytesShifted happen to match (coincidental)
    # We shift at least one character up to a max of MAX_SHIFTS_TO_ANALYZE characters
    # When the shift is equal to the length of the key, the bytes compared will have been encyrypted by
    # the same key and will be statistically more likely to be the same character. (About twice as likely)
    # These "bumps" will be evident in the histogram with a period equal to the length of the key

    MAX_SHIFTS_TO_ANALYZE = 50

    lBytesOfInput = len(pInput)
    lShiftsToAnalyze = min(lBytesOfInput, MAX_SHIFTS_TO_ANALYZE)
    lIOC = dict.fromkeys(range(1, lShiftsToAnalyze), 0)
    for lBytesShifted in range(1, lShiftsToAnalyze):
        lMatches = 0
        lBytesToTest = lBytesOfInput - lBytesShifted
        for lByte in range(0, lBytesToTest):
            if pInput[lByte] == pInput[lByte + lBytesShifted]:
                lMatches += 1
            # end if
        # end for lByte
        # Dividing denominator by bytes in alphabet normalizes IOC
        lIOC[lBytesShifted] = lMatches / (lBytesToTest / MODULUS)
    # end for lBytesShifted

    return lIOC


def print_kappa_index_of_coincidence(pInput: bytearray, pVerbose) -> None:
    lIOC = get_kappa_index_of_coincidence(pInput)

    lScaleFactor = 20

    for lByteOffset, lCoincidence in lIOC.items():
        lCoincidenceBarLength = int(lCoincidence * lScaleFactor)

        lOutput = ""
        if pVerbose:
            lOutput = 'Byte Offset: '
        lOutput += str(lByteOffset).zfill(2) + ' '
        lOutput += "[" + TWO_DECIMAL_PLACES.format(lCoincidence) + "] "
        lOutput += "#" * lCoincidenceBarLength
        print(lOutput)
    # end for


def print_byte_analysis(pByte: int, pByteCount: int, pTotalBytes: int, pShowCount: bool, pShowHistogram: bool, pShowASCII: bool, pShowPercent: bool, pVerbose: bool) -> None:
    SCALE_FACTOR = 20
    lPercent = pByteCount / pTotalBytes * 100
    lFrequencyBarLength = int(lPercent * SCALE_FACTOR)
    lByteString = str(pByte)
    lByteStringLength = len(lByteString)

    if pVerbose and lByteStringLength < 2:
        lByteTab = '\t\t'
    else:
        lByteTab = '\t'

    lOutput = ''
    if pVerbose:
        lOutput = 'Byte: '
    lOutput += lByteString + lByteTab
    if pShowASCII:
        lOutput += chr(pByte) + '\t'
    if pShowCount:
        lOutput += str(pByteCount) + '\t'
    if pShowPercent:
        lOutput += "(" + TWO_DECIMAL_PLACES.format(lPercent) + "%)\t"
    if pShowHistogram:
        lOutput += "#" * lFrequencyBarLength
    print(lOutput)
    # end if


def print_analysis(pInput: bytearray, pShowCount: bool, pShowHistogram: bool, pShowASCII: bool, pShowPercent: bool, pShowGuesses: bool, pVerbose: bool, pTopFrequencies: int, pKeyLength: int) -> None:

    lByteCounts, lTotalBytes = get_byte_counts(pInput)

    print()
    print("Analysis of Input")

    if pTopFrequencies:
        lBytesPrinted = 0
        lAnalyzingMostPopularByte = True
        for lByte, lByteCount in sorted(lByteCounts.items(), key=lambda x:x[1], reverse=True):
            if pVerbose or lByteCount:
                if pShowGuesses and lAnalyzingMostPopularByte:
                    # For JPEG we assume the mode of the plaintext is 0,
                    # so we guess the mode of the cipher text is offset by X bytes
                    print('\nBest guess\tLowercase: ' + chr((lByte + 97) % MODULUS) + '\tUppercase: ' + chr((lByte + 65) % MODULUS) + '\tNumeric: ' + chr((lByte + 48) % MODULUS))
                    lAnalyzingMostPopularByte = False
                # end if
                print_byte_analysis(lByte, lByteCount, lTotalBytes, pShowCount, pShowHistogram, pShowASCII, pShowPercent, pVerbose)
            # end if
            lBytesPrinted += 1
            if lBytesPrinted > (pTopFrequencies - 1):
                break
        # end for
    else:
        for lByte, lByteCount in lByteCounts.items():
            if pVerbose or lByteCount:
                print_byte_analysis(lByte, lByteCount, lTotalBytes, pShowCount, pShowHistogram, pShowASCII, pShowPercent, pVerbose)
            # end if
        # end for


def print_columnar_analysis(pInput: bytearray, pShowCount: bool, pShowHistogram: bool, pShowASCII: bool, pShowPercent: bool, pShowGuesses: bool, pVerbose: bool, pTopFrequencies: int, pKeyLength: int) -> None:

    lColumns = {lColumn: bytearray() for lColumn in range(0, pKeyLength)}
    lColumn = 0
    for lByte in lInput:
        lColumns[lColumn].append(lByte)
        lColumn = (lColumn + 1) % pKeyLength

    for lColumn in lColumns:
        print("Analysis of Column {}".format(lColumn + 1))
        print_analysis(lColumns[lColumn], lArgs.show_count, lArgs.show_histogram, lArgs.show_ascii, lArgs.show_percent,
                       lArgs.show_guesses, lArgs.verbose, lArgs.top_frequencies, lArgs.columnar_analysis)
        print()


def print_mean(pMean: float, pVerbose: bool) -> None:
    if pVerbose:
        print()
        print("Arithmetic Mean (Average): {}".format(TWO_DECIMAL_PLACES.format(pMean)))
    else:
        print(TWO_DECIMAL_PLACES.format(pMean))


def print_median(pMedian: int, pVerbose: bool) -> None:
    if pVerbose:
        print()
        print("Median (Middle element): {}".format(pMedian))
    else:
        print(pMedian)


def print_mode(pMode: int, pModeCount: int, pModeCountRatio: int, pVerbose: bool) -> None:
    if pVerbose:
        print()
        print("Mode (Most populous): {} (Count: {} Ratio: {})".format(pMode, pModeCount, TWO_DECIMAL_PLACES.format(pModeCountRatio)))
    else:
        print(pMode)


def print_anti_mode(pAntiMode: int, pAntiModeCount: int, pAntiModeCountRatio: int, pVerbose: bool) -> None:
    if pVerbose:
        print()
        print("Anti-Mode (Least populous): {} (Count: {} Ratio: {})".format(pAntiMode, pAntiModeCount, TWO_DECIMAL_PLACES.format(pAntiModeCountRatio)))
    else:
        print(pAntiMode)


def print_variance(pVariance: float, pVerbose: bool) -> None:
    if pVerbose:
        print()
        print("Variance: {}".format(TWO_DECIMAL_PLACES.format(pVariance)))
    else:
        print(TWO_DECIMAL_PLACES.format(pVariance))


def print_standard_deviation(pStandardDeviation: float, pVerbose: bool) -> None:
    if pVerbose:
        print()
        print("Standard Deviation: {}".format(TWO_DECIMAL_PLACES.format(pStandardDeviation)))
    else:
        print(TWO_DECIMAL_PLACES.format(pStandardDeviation))


def print_entropy(pByteCounts: dict, pTotalBytes: int, pVerbose: bool) -> None:
    lEntropy = get_entropy(pByteCounts, pTotalBytes)
    if pVerbose:
        print()
        print("Entropy: {}".format(TWO_DECIMAL_PLACES.format(lEntropy)))
    else:
        print(TWO_DECIMAL_PLACES.format(lEntropy))


if __name__ == '__main__':

    lArgParser = argparse.ArgumentParser(description='Freek: An implementation of a frequency and cryptography analyzer.',
                                         epilog='For each byte in file encrypted-funny-cat-1.jpg, show count, percent and histogram.\n\npython freak.py -cpm --verbose -i encrypted-funny-cat-1.jpg\n\nFor each byte in file encrypted-funny-cat-1.jpg, show count, percent, histogram and all statistics\n\npython freak.py --show-all --verbose -i encrypted-funny-cat-1.jpg\n\nFor each byte in file encrypted-funny-cat-1.jpg, show all statistics: mean, median, mode, anti-mode, variance, standard deviation, and Shannon entropy\n\npython freak.py --show-statistics --verbose -i encrypted-funny-cat-1.jpg\n\nDetermine the index of coincidence of file encrypted-funny-cat-1.jpg in order to determine the length of a Vigenere password. This only works if the input file is encrypted with the Vigenere file.\n\npython freak.py -ioc --verbose --input-file=encrypted-funny-cat-1.bin\n\nFor each byte in file encrypted-funny-cat-1.jpg, group input into columns. For example, -col 5 groups together byte 1, 6, 11, etc. Analysis is performed independently on each column.\n\npython freak.py -cpm -col 8 --input-file=encrypted-funny-cat-1.bin\n\nFor each byte in file encrypted-funny-cat-1.jpg, group input into columns. For example, -col 5 groups together byte 1, 6, 11, etc. Analysis is performed independently on each column. -t sorts the results then only shows top t results. In this example, the top 5 results.\n\npython freak.py -cpm -col 8 -t 5 --input-file=encrypted-funny-cat-1.bin\n\nTo guess a Vigenere password of length "col", add -g option. This only works if output is grouped into columns first. This example assumes the password is 8 characters long.\n\npython freak.py -cpm -g -t 1 -col 8 --input-file=encrypted-funny-cat-1.bin',
                                         formatter_class=RawTextHelpFormatter)

    lOutputOptions = lArgParser.add_argument_group(title="Histogram Options", description="Choose the type(s) of histogram output to display")
    lOutputOptions.add_argument('-c', '--show-count', help='Show count for each byte of input', action='store_true')
    lOutputOptions.add_argument('-p', '--show-percent', help='Show percent representation for each byte of input', action='store_true')
    lOutputOptions.add_argument('-m', '--show-histogram', help='Show histogram for each byte of input', action='store_true')
    lOutputOptions.add_argument('-a', '--show-ascii', help='Show ASCII representation for each byte of input', action='store_true')
    lOutputOptions.add_argument('-all', '--show-all', help='Show statistics, count, ASCII, percent represenation, histogram for each byte of input and Shannon entropy for input. Does NOT include index of coincidence or show ascii. Equivalent to -cpme -mean -median -mode -variance -stddev.', action='store_true')

    lStatisticsOptions = lArgParser.add_argument_group(title="Statistics Options", description="Choose the type(s) of statistical output to display")

    lStatisticsOptions.add_argument('-mean', '--show-mean', help='Show Arithmetic Mean (Average)', action='store_true')
    lStatisticsOptions.add_argument('-median', '--show-median', help='Show Median', action='store_true')
    lStatisticsOptions.add_argument('-mode', '--show-mode', help='Show Mode (Most popular byte)', action='store_true')
    lStatisticsOptions.add_argument('-antimode', '--show-anti-mode', help='Show Anti-Mode (Least popular byte)', action='store_true')
    lStatisticsOptions.add_argument('-variance', '--show-variance', help='Show Variance', action='store_true')
    lStatisticsOptions.add_argument('-stddev', '--show-standard-deviation', help='Show Standard Deviation', action='store_true')
    lStatisticsOptions.add_argument('-e', '--show-entropy', help='Show Shannon entropy', action='store_true')
    lStatisticsOptions.add_argument('-stats', '--show-statistics', help='Show mean, median, mode, variance and standard deviation for each byte of input and Shannon entropy for input. Equivalent to -e -mean -median -mode -variance -stddev.', action='store_true')

    lIOCOptions = lArgParser.add_argument_group(title="Index of Coincidence Options", description="Choose the type(s) of IOC output to display")

    lIOCOptions.add_argument('-ioc', '--show-ioc', help='Show kappa index of coincidence', action='store_true')

    lColumnarAnalysisOptions = lArgParser.add_argument_group(title="Columnar Analysis Options", description="Choose the type(s) of output to display")

    lColumnarAnalysisOptions.add_argument('-t', '--top-frequencies', help='Only display top X frequencies. Particuarly useful when combined with columnar analysis, histogram or when less important bytes clutter analysis.', action='store', type=int)
    lColumnarAnalysisOptions.add_argument('-g', '--show-guesses', help='Show ascii representation for top byte of input. Tries ASCII lower, upper and numeric translations. Only works with -t/--top-frequencies.', action='store_true')
    lColumnarAnalysisOptions.add_argument('-col', '--columnar-analysis', help='Break INPUT into X columns and perform analysis on columns. Particuarly useful against polyalphabetic stream ciphers.', action='store', type=int)

    lOtherOptions = lArgParser.add_argument_group(title="Other Options", description="Choose other options")

    lOtherOptions.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
    lOtherOptions.add_argument('-if', '--input-format', help='Input format can be character, binary, or base64', choices=['character', 'binary', 'base64'], default='character', action='store', type=str)

    lInputSource = lArgParser.add_mutually_exclusive_group(required='True')
    lInputSource.add_argument('-i', '--input-file', help='Read INPUT to analyze from an input file', action='store', type=str)
    lInputSource.add_argument('INPUT', nargs='?', help='INPUT to analyze', action='store')
    lArgs = lArgParser.parse_args()

    if lArgs.show_statistics:
        lArgs.show_entropy = lArgs.show_mean = lArgs.show_median = lArgs.show_mode = lArgs.show_anti_mode = lArgs.show_variance = lArgs.show_standard_deviation = True

    if lArgs.show_all:
        lArgs.show_percent = lArgs.show_histogram = lArgs.show_count = lArgs.show_entropy = lArgs.show_mean = lArgs.show_median = lArgs.show_mode = lArgs.show_anti_mode = lArgs.show_variance = lArgs.show_standard_deviation = True

    if lArgs.show_percent is False and lArgs.show_histogram is False \
            and lArgs.show_ascii is False and lArgs.show_count is False and lArgs.show_ioc is False \
            and lArgs.show_entropy is False and lArgs.show_mean is False and lArgs.show_median is False \
            and lArgs.show_mode is False and lArgs.show_anti_mode is False and lArgs.show_variance is False and lArgs.show_standard_deviation is False:
        lArgParser.error('No output chosen to display. Please choose at least one output option.')

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
    # end if

    if lArgs.show_percent or lArgs.show_histogram or lArgs.show_ascii or lArgs.show_count:

        if lArgs.columnar_analysis:
            print_columnar_analysis(lInput, lArgs.show_count, lArgs.show_histogram, lArgs.show_ascii, lArgs.show_percent, lArgs.show_guesses, lArgs.verbose, lArgs.top_frequencies, lArgs.columnar_analysis)
        else:
            print_analysis(lInput, lArgs.show_count, lArgs.show_histogram, lArgs.show_ascii, lArgs.show_percent, lArgs.show_guesses, lArgs.verbose, lArgs.top_frequencies, lArgs.columnar_analysis)

    if lArgs.show_ioc:
        print_kappa_index_of_coincidence(lInput, lArgs.verbose)

    if lArgs.show_mean or lArgs.show_median or lArgs.show_mode or lArgs.show_anti_mode or lArgs.show_variance or lArgs.show_standard_deviation:
        lMean, lMeadian, lMode, lModeCount, lModeCountRatio, lAntiMode, lAntiModeCount, lAntiModeCountRatio, lVariance, lStandardDeviation = get_statistics(lInput)

    if lArgs.show_mean:
        print_mean(lMean, lArgs.verbose)

    if lArgs.show_median:
        print_median(lMeadian, lArgs.verbose)

    if lArgs.show_mode:
        print_mode(lMode, lModeCount, lModeCountRatio, lArgs.verbose)

    if lArgs.show_anti_mode:
        print_anti_mode(lAntiMode, lAntiModeCount, lAntiModeCountRatio, lArgs.verbose)

    if lArgs.show_variance:
        print_variance(lVariance, lArgs.verbose)

    if lArgs.show_standard_deviation:
        print_standard_deviation(lStandardDeviation, lArgs.verbose)

    if lArgs.show_entropy:
        lByteCounts, lTotalBytes = get_byte_counts(lInput)
        print_entropy(lByteCounts, lTotalBytes, lArgs.verbose)
