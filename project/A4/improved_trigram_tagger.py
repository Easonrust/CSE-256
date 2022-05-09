import sys
from collections import defaultdict
import math
import itertools


def read_counts(counts_file, word_tag, word_dict, ngram_tag):
    for l in counts_file:
        line = l.strip().split(' ')
        if line[1] == 'WORDTAG':
            word_tag[(line[3], line[2])] = int(line[0])
            word_dict.append(line[3])
        else:
            ngram_tag[tuple(line[2:])] = int(line[0])


def calculate_e_parameter(word_tag, word_dict, ngram_tag, x, y):
    if x in word_dict:
        return float(word_tag[(x, y)]) / float(ngram_tag[(y,)])
    else:
        rare_class = "_RARE_"
        if x.isnumeric():
            rare_class = "_RARE_NUM_"
        # if x.isalpha() and x.isupper():
        #     rare_class = "_RARE_ALUP_"
        # if x.isalpha() and x.islower():
        #     rare_class = "_RARE_ALLOW_"
        if x.isalpha():
            rare_class = "_RARE_AL_"
        if not x.isalnum():
            rare_class = "_RARE_PUNCT_"
        return float(word_tag[(rare_class, y)]) / float(ngram_tag[(y,)])


def calculate_q_parameter(ngram_tag, v, w, u):
    return float(ngram_tag[w, u, v]) / float(ngram_tag[w, u])


def viterbi(word_tag, word_dict, ngram_tag, word_list):
    n = len(word_list)
    tag_set = ('O', 'I-GENE')
    bp = {}
    pi = {(0, '*', '*'): 1}

    # dynamic programming with backpointers
    for k in range(1, n+1):
        s_k_1 = tag_set
        s_k_2 = tag_set
        s_k = tag_set
        if k == 1:
            s_k_1 = ('*')
            s_k_2 = ('*')
        elif k == 2:
            s_k_2 = ('*')
        for u in s_k_1:
            for v in s_k:
                e = calculate_e_parameter(
                    word_tag, word_dict, ngram_tag, word_list[k-1], v)
                max_pi = -100
                max_bp = '*'
                for w in s_k_2:
                    if max_pi < (pi[k - 1, w, u] * calculate_q_parameter(ngram_tag, v, w, u) * e):
                        max_pi = (pi[k - 1, w, u] *
                                  calculate_q_parameter(ngram_tag, v, w, u) * e)
                        max_bp = w
                pi[k, u, v] = max_pi
                bp[k, u, v] = max_bp

    uv_list = [(pi[n, u, v] * calculate_q_parameter(ngram_tag,
                'STOP', u, v), (u, v)) for (u, v) in itertools.product(tag_set, tag_set)]
    tag_n_1, tag_n = max(uv_list, key=lambda x: x[0])[1]
    tag_list = [0] * (n+1)
    tag_list[n-1] = tag_n_1
    tag_list[n] = tag_n
    for i in range(n-2, 0, -1):
        tag_list[i] = bp[i + 2, tag_list[i + 1], tag_list[i + 2]]
    return tag_list[1:]


def tag_gene(word_tag, word_dict, ngram_tag, out_f, dev_file):
    word_list = []
    for l in dev_file:
        line = l.strip()
        if line:
            word_list.append(line)
        else:
            tag_list = viterbi(word_tag, word_dict, ngram_tag, word_list)
            for word, tag in zip(word_list, tag_list):
                out_f.write("%s %s\n" % (word, tag))
            out_f.write('\n')
            word_list = []
    out_f.close()


def usage():
    print("""
    python improved_trigram_tagger.py [input_file_1] [input_file_2] > [output_file]
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

    word_tag, ngram_tag = defaultdict(int), defaultdict(int)
    word_dict = []

    read_counts(counts_file, word_tag, word_dict, ngram_tag)
    counts_file.close()
    tag_gene(word_tag, word_dict, ngram_tag, sys.stdout, dev_file)
    dev_file.close()
