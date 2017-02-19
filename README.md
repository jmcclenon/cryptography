# Shifty

An Implementation of Shift Cipher

Usage: shifty.py [-h] (-e | -d) (-k KEY | -b) [-if {character,binary,base64}]
                 [-of {character,binary,base64}] [-v] [-i INPUT_FILE]
                 [INPUT]

Required arguments:
  
    INPUT                 Input value to encrypt/decrypt

Optional arguments:

    -h, --help            show this help message and exit
    -e, --encrypt         Encrypt INPUT. This option requires a KEY.
    -d, --decrypt         Decrypt INPUT. This option requires a KEY or
                        BRUTEFORCE flag.
    -k KEY, --key KEY     Encryption/Decription key
    -b, --bruteforce      Rather than decrypt with KEY, try to brute force the
                        plaintext.
    -if {character,binary,base64}, --input-format {character,binary,base64}
                        Input format can be character, binary, or base64
    -of {character,binary,base64}, --output-format {character,binary,base64}
                        Output format can be character, binary, or base64
    -m MODULUS, --modulus MODULUS
                        Modulus. Default is 256.
    -v, --verbose         Enables verbose output
    -i INPUT_FILE, --input-file INPUT_FILE
                        Read INPUT from an input file

# Affinity

    An implementation of Affine Cipher

Usage: affinity.py [-h] (-e | -d) -k KEY [-if {character,binary,base64}]
                   [-of {character,binary,base64}] [-v] [-i INPUT_FILE]
                   [INPUT]

Required arguments:

    INPUT                 Input value to encrypt/decrypt

Optional arguments:

    -h, --help            show this help message and exit
    -e, --encrypt         Encrypt INPUT. This option requires a KEY.
    -d, --decrypt         Decrypt INPUT. This option requires a KEY or
                        BRUTEFORCE flag.
    -k KEY, --key KEY     Encryption/Decryption key in a,b format
    -if {character,binary,base64}, --input-format {character,binary,base64}
                        Input format can be character, binary, or base64
    -of {character,binary,base64}, --output-format {character,binary,base64}
                        Output format can be character, binary, or base64
    -m MODULUS, --modulus MODULUS
                        Modulus. Default is 256.
    -v, --verbose         Enables verbose output
    -i INPUT_FILE, --input-file INPUT_FILE
                        Read INPUT from an input file

# Visionary

    An implementation of Vigenère Cipher

Usage: visionary.py [-h] (-e | -d) -k KEY [-if {character,binary,base64}]
                    [-of {character,binary,base64}] [-v] [-i INPUT_FILE]
                    [INPUT]

Required arguments:
    
    INPUT                 Input value to encrypt/decrypt

Optional arguments:

    -h, --help            show this help message and exit
    -e, --encrypt         Encrypt INPUT. This option requires a KEY.
    -d, --decrypt         Decrypt INPUT. This option requires a KEY or
                        BRUTEFORCE flag.
    -k KEY, --key KEY     Encryption/Decryption key
    -if {character,binary,base64}, --input-format {character,binary,base64}
                        Input format can be character, binary, or base64
    -of {character,binary,base64}, --output-format {character,binary,base64}
                        Output format can be character, binary, or base64
    -m MODULUS, --modulus MODULUS
                        Modulus. Default is 256.
    -v, --verbose         Enables verbose output
    -i INPUT_FILE, --input-file INPUT_FILE
                        Read INPUT from an input file

# Substitute

    An implementation of Substitution Cipher
    
Usage: substitute.py [-h] (-e | -d) -k KEY [-if {character,binary,base64}]
                     [-of {character,binary,base64}] [-v] [-i INPUT_FILE]
                     [INPUT]

Required arguments:
  INPUT                 Input value to encrypt/decrypt

Optional arguments:

    -h, --help            show this help message and exit
    -e, --encrypt         Encrypt INPUT. This option requires a KEY.
    -d, --decrypt         Decrypt INPUT. This option requires a KEY.
    -k KEY, --key KEY     Encryption/Decryption key
    -if {character,binary,base64}, --input-format {character,binary,base64}
                        Input format can be character, binary, or base64
    -of {character,binary,base64}, --output-format {character,binary,base64}
                        Output format can be character, binary, or base64. If
                        input format provided, but output format is not
                        provided, output format defaults to match input
                        format.
    -v, --verbose         Enables verbose output
    -i INPUT_FILE, --input-file INPUT_FILE
                        Read INPUT from an input file
                        
# Freek

    Byte frequency analyzer

Usage: freek.py [-h] [-c] [-p] [-m] [-a] [-ioc] [-all] [-t TOP_FREQUENCIES]
                [-g] [-col COLUMNAR_ANALYSIS] [-v]
                [-if {character,binary,base64}] [-i INPUT_FILE]
                [INPUT]

Required arguments:
    
    INPUT                 INPUT to analyze

Optional arguments:

    -h, --help            show this help message and exit
    -t TOP_FREQUENCIES, --top-frequencies TOP_FREQUENCIES
                        Only display top X frequencies. Particuarly useful
                        when combined with columnar analysis or when less
                        important bytes clutter analysis.
    -g, --show-guesses    Show ascii representation for top byte of input. Tries
                        ASCII lower, upper and numeric translations. Only
                        works with -t/--top-frequencies.
    -col COLUMNAR_ANALYSIS, --columnar-analysis COLUMNAR_ANALYSIS
                        Break INPUT into X columns and perform analysis on
                        columns. Particuarly useful against polyalphabetic
                        stream ciphers.
    -v, --verbose         Enables verbose output
    -if {character,binary,base64}, --input-format {character,binary,base64}
                        Input format can be character, binary, or base64
    -i INPUT_FILE, --input-file INPUT_FILE
                        Read INPUT to analyze from an input file
    
    Output Options:
    Choose the type(s) of output to display
    
    -c, --show-count      Show count for each byte of input
    -p, --show-percent    Show percent representation for each byte of input
    -m, --show-histogram  Show histogram for each byte of input
    -a, --show-ascii      Show ascii representation for each byte of input
    -e, --show-entropy    Show Shannon entropy
    -ioc, --show-ioc      Show kappa (delta) index of coincidence
    -all, --show-all      Show count, ascii, percent represenation, histogram
                        for each byte of input and Shannon entropy for input.
                        Does NOT include index of coincidence. Equivalent to
                        -cpmae.

# Inversion

    Inverts elements modulo a modulus

Usage: inversion.py [-h] [-i] [-m MODULUS] [-v] INPUT

Required arguments:

    INPUT                 Integer input value of which to calculate inverse. Required.

Optional arguments:

    -h, --help            show this help message and exit
    -i, --mutiplicative-inverse
                        Calculate multiplicative inverse of INPUT modulo
                        MODULUS
    -m MODULUS, --modulus MODULUS
                        Modulus. Default is 256.
    -v, --verbose         Enables verbose output

# Maitre D

A matrix variant calculator within modulo MODULUS

Usage: maitred.py [-h] [-d] [-id] [-mi] [-c] [-a] [-i] [-all] [-v]
                  [-m MODULUS]
                  [INPUT]

Required arguments:

    INPUT                 Input matrix of integers. The matrix must be square.
                        For example a 2 X 2 matrix could be 1, 2, 3, 4

Optional arguments:

    -h, --help            show this help message and exit
    -d, --determinant     Calculate the determinant of the matrix modulo
                        MODULUS. Answer will be in Z-MODULUS.
    -id, --inverse-determinant
                        Calculate the inverse of the determinant of the matrix
                        modulo MODULUS. Answer will be in Z-MODULUS.
    -mi, --minors         Calculate the minors of the matrix modulo MODULUS
    -c, --cofactors       Calculate the cofactors of the matrix modulo MODULUS
    -a, --adjunct         Calculate the adjunct of the matrix modulo MODULUS
    -i, --inverse         Calculate the inverse of the matrix modulo MODULUS
    -all, --all           Calculate the determinant, inverse determinant,
                        adjunct and inverse of the matrix modulo MODULUS. Same
                        as -id -dai
    -v, --verbose         Enables verbose output
    -m MODULUS, --modulus MODULUS
                        Modulus. Default is 256.