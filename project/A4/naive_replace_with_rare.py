import sys
from collections import defaultdict


def read_counts(corpusfile):
    word_counts = defaultdict(int)

    for l in corpusfile:
        line = l.strip()
        if line:
            lineArr = line.split(' ')
            if (lineArr[0]) in word_counts:
                word_counts[(lineArr[0])] += 1
            else:
                word_counts[(lineArr[0])] = 1
    return word_counts


def replace_with_rare(corpusfile, output, word_counts):
    for l in corpusfile:
        line = l.strip()
        if line:
            lineArr = line.split(' ')
            if word_counts[lineArr[0]] < 5:
                output.write("_RARE_ %s\n" % (lineArr[1]))
            else:
                output.write(line + "\n")
        else:
            output.write("\n")


def usage():
    print("""
    python naive_replace_with_rare.py [input_file] > [output_file]
        Read in a gene tagged training input file and replace the rare or unseen word with single rare class.
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
