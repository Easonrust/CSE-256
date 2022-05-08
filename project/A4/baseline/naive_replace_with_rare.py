'''
@Author: 
@Date: 2019-11-01 19:58:55
@LastEditors: Shihan Ran
@LastEditTime: 2019-11-01 21:06:03
@Email: rshcaroline@gmail.com
@Software: VSCode
@License: Copyright(C), UCSD
@Description: 
'''

import sys
from collections import defaultdict


threshold = 5


def read_counts(corpusfile):
    """
    Read the corpusfile and return word counts
    """
    word_counts = defaultdict(int)

    for l in corpusfile:
        line = l.strip()
        if line:
            linew = line.split(' ')
            if (linew[0]) in word_counts:
                word_counts[(linew[0])] += 1
            else:
                word_counts[(linew[0])] = 1
    return word_counts


def replace_with_rare(corpusfile, output, word_counts):
    """
    Read the corpus_file and replace rare words with rare word classes
    """
    for l in corpusfile:
        line = l.strip()
        if line:
            linew = line.split(' ')
            if word_counts[linew[0]] < threshold:
                output.write("_RARE_ %s\n" % (linew[1]))
            else:
                output.write(line + "\n")
        else:
            output.write("\n")


def usage():
    print("""
    python ./replace_with_rare.py [input_file] > [output_file]
        Read in a gene tagged training input file and produce new training file.
    """)


if __name__ == "__main__":
    if len(sys.argv) != 2:  # Expect exactly one argument: the training data file
        usage()
        sys.exit(2)
    try:
        input = open(sys.argv[1], "r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)
    word_counts = read_counts(input)
    input.close()

    try:
        input = open(sys.argv[1], "r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)
    replace_with_rare(input, sys.stdout, word_counts)
