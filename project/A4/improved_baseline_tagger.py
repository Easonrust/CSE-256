import sys
from collections import defaultdict
import math


def read_counts(counts_file, emission_counts, word_dict, unigram_counts):
    for l in counts_file:
        line = l.strip().split(' ')
        if line[1] == 'WORDTAG':
            emission_counts[(line[3], line[2])] = int(line[0])
            word_dict.append(line[3])
        elif line[1] == '1-GRAM':
            unigram_counts[(line[2])] = int(line[0])


def compute_e_parameter(emission_counts, unigram_counts, word, tag):
    return float(emission_counts[(word, tag)]) / float(unigram_counts[(tag)])


def calculate_max_emission_parameter(emission_counts, word_dict, unigram_counts, max_emission_parameter):
    for word in word_dict:
        max_tag = ''
        max_val = 0.0
        for tag in unigram_counts:
            if compute_e_parameter(emission_counts, unigram_counts, word, tag) > max_val:
                max_val = float(
                    emission_counts[(word, tag)]) / float(unigram_counts[(tag)])
                max_tag = tag
        max_emission_parameter[(word)] = max_tag


def tag_gene(emission_parameter, out_f, dev_file):
    for l in dev_file:
        line = l.strip()
        if line:
            if line in emission_parameter:
                out_f.write("%s %s\n" % (line, emission_parameter[(line)]))
            else:
                rare_class = "_RARE_"
                if line[0].isnumeric():
                    rare_class = "_RARE_NUM_"
                if line[0].isalpha() and line[0].isupper():
                    rare_class = "_RARE_ALUP_"
                if line[0].isalpha() and line[0].islower():
                    rare_class = "_RARE_ALLOW_"
                # if line[0].isalpha():
                #     rare_class = "_RARE_AL_"
                # if line[0].isalnum():
                #     rare_class = "_RARE_ALNUM_"
                if not line[0].isalnum():
                    rare_class = "_RARE_PUNCT_"
                out_f.write("%s %s\n" %
                            (line, emission_parameter[(rare_class)]))
        else:
            out_f.write("\n")


def usage():
    print("""
    python improved_baseline_tagger.py [input_file_1] [input_file_2] > [output_file]
        Read in counts file and dev file, output tagging results.
    """)


if __name__ == "__main__":

    if len(sys.argv) != 3:  # Expect exactly one argument: the training data file
        usage()
        sys.exit(2)

    try:
        counts_file = open(sys.argv[1], "r")
        dev_file = open(sys.argv[2], 'r')
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)

    emission_counts, unigram_counts, max_emission_parameter = defaultdict(
        int), defaultdict(int), defaultdict(int)
    word_dict = []

    read_counts(counts_file, emission_counts, word_dict, unigram_counts)
    counts_file.close()
    calculate_max_emission_parameter(
        emission_counts, word_dict, unigram_counts, max_emission_parameter)
    tag_gene(max_emission_parameter, sys.stdout, dev_file)
    dev_file.close()
