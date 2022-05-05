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
                max_val = float(emission_counts[(word, tag)]) / float(unigram_counts[(tag)])
                max_tag = tag
        max_emission_parameter[(word)] = max_tag

def tag_gene(emission_parameter, out_f, dev_file):
    for l in dev_file:
        line = l.strip()
        if line:
            if line in emission_parameter:
                out_f.write("%s %s\n" % (line, emission_parameter[(line)]))
            else:
                out_f.write("%s %s\n" % (line, emission_parameter[('_RARE_')]))
        else:
            out_f.write("\n")

def usage():
    print ("""
    python baseline.py [input_train_counts] [input_dev_file] > [output_file]
        Read in counts file and dev file, produce tagging results.
    """)


if __name__ == "__main__":

    if len(sys.argv)!=3: # Expect exactly one argument: the training data file
        usage()
        sys.exit(2)

    try:
        counts_file = open(sys.argv[1], "r")
        dev_file = open(sys.argv[2], 'r')
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)
        
    emission_counts, unigram_counts, max_emission_parameter = defaultdict(int), defaultdict(int), defaultdict(int)
    word_dict = []

    read_counts(counts_file, emission_counts, word_dict, unigram_counts)
    counts_file.close()
    calculate_max_emission_parameter(emission_counts, word_dict, unigram_counts, max_emission_parameter)
    tag_gene(max_emission_parameter, sys.stdout, dev_file)
    dev_file.close()