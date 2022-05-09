import sys
from collections import defaultdict


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
            if word_counts[linew[0]] < 5:
                rare_class = "_RARE_"
                if linew[0].isnumeric():
                    rare_class = "_RARE_NUM_"
                # if linew[0].isalpha() and linew[0].isupper():
                #     rare_class = "_RARE_ALUP_"
                # if linew[0].isalpha() and linew[0].islower():
                #     rare_class = "_RARE_ALLOW_"
                if linew[0].isalpha():
                    rare_class = "_RARE_AL_"
                # if linew[0].isalnum():
                #     rare_class = "_RARE_ALNUM_"
                if not linew[0].isalnum():
                    rare_class = "_RARE_PUNCT_"
                output.write(rare_class+" %s\n" % (linew[1]))
            else:
                output.write(line + "\n")
        else:
            output.write("\n")


def usage():
    print("""
    python improved_replace_with_rare.py [input_file] > [output_file]
        Read in a gene tagged training input file and replace the rare or unseen word with multiple rare classes.
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
