#!/bin/python

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import collections
from math import log
import sys

# Python 3 backwards compatibility tricks
if sys.version_info.major > 2:

    def xrange(*args, **kwargs):
        return iter(range(*args, **kwargs))

    def unicode(*args, **kwargs):
        return str(*args, **kwargs)


class LangModel:
    def fit_corpus(self, corpus):
        """Learn the language model for the whole corpus.

        The corpus consists of a list of sentences."""
        for s in corpus:
            self.fit_sentence(s)
        self.norm()

    def perplexity(self, corpus):
        """Computes the perplexity of the corpus by the model.

        Assumes the model uses an EOS symbol at the end of each sentence.
        """
        return pow(2.0, self.entropy(corpus))

    def entropy(self, corpus):
        num_words = 0.0
        sum_logprob = 0.0
        for s in corpus:
            num_words += len(s) + 1  # for EOS
            sum_logprob += self.logprob_sentence(s)
        return -(1.0/num_words)*(sum_logprob)

    def logprob_sentence(self, sentence):
        p = 0.0
        for i in xrange(len(sentence)):
            p += self.cond_logprob(sentence[i], sentence[:i])
        p += self.cond_logprob('END_OF_SENTENCE', sentence)
        return p

    # required, update the model when a sentence is observed
    def fit_sentence(self, sentence): pass
    # optional, if there are any post-training steps (such as normalizing probabilities)
    def norm(self): pass
    # required, return the log2 of the conditional prob of word, given previous words
    def cond_logprob(self, word, previous): pass
    # required, the list of words the language model suports (including EOS)
    def vocab(self): pass


class Unigram(LangModel):
    def __init__(self, backoff=0.000001):
        self.model = dict()
        self.lbackoff = log(backoff, 2)

    def inc_word(self, w):
        if w in self.model:
            self.model[w] += 1.0
        else:
            self.model[w] = 1.0

    def fit_sentence(self, sentence):
        for w in sentence:
            self.inc_word(w)
        self.inc_word('END_OF_SENTENCE')

    def norm(self):
        """Normalize and convert to log2-probs."""
        tot = 0.0
        for word in self.model:
            tot += self.model[word]
        ltot = log(tot, 2)
        for word in self.model:
            self.model[word] = log(self.model[word], 2) - ltot

    def cond_logprob(self, word, previous):
        if word in self.model:
            return self.model[word]
        else:
            return self.lbackoff

    def vocab(self):
        return self.model.keys()


class Trigram(LangModel):
    def __init__(self, backoff=0.001, delta=0.001, smoothing=True):
        self.model = dict()
        self.bigram = dict()
        self.unigram = dict()
        self.delta = delta
        self.smoothing = smoothing
        self.lbackoff = log(backoff, 2)

    def inc_trigram(self, t):
        if t in self.model.keys():
            self.model[t] += 1.0
        else:
            self.model[t] = 1.0

    def inc_bigram(self, b):
        if b in self.bigram.keys():
            self.bigram[b] += 1.0
        else:
            self.bigram[b] = 1.0

    def inc_word(self, w):
        if w in self.unigram.keys():
            self.unigram[w] += 1.0
        else:
            self.unigram[w] = 1.0

    def fit_sentence(self, sentence):
        sentence = ['*', '*'] + sentence + ['END_OF_SENTENCE']
        trigram_list = [' '.join(sentence[i:i+3])
                        for i in range(len(sentence)-2)]
        bigram_list = [' '.join(sentence[i:i+2])
                       for i in range(len(sentence)-1)]

        for t in trigram_list:
            self.inc_trigram(t)

        for b in bigram_list:
            self.inc_bigram(b)

        for u in sentence:
            self.inc_word(u)
        self.inc_word('END_OF_SENTENCE')

    def norm(self):
        """Normalize and convert to log2-probs."""
        for t in self.model:
            b = ' '.join(t.split(' ')[:2])
            if self.smoothing:
                self.model[t] = log(self.model[t]+self.delta, 2) - \
                    log(self.bigram[b]+self.delta *
                        len(self.unigram), 2)
            else:
                self.model[t] = log(self.model[t], 2) - \
                    log(self.bigram[b], 2)

    def cond_logprob(self, word, previous):
        tri_sentence = ''
        if not previous:
            tri_sentence = ' '.join(['*', '*', word])
        elif len(previous) == 1:
            tri_sentence = ' '.join(['*', previous[0], word])
        else:
            tri_sentence = ' '.join(previous[-2:]+[word])

        if tri_sentence in self.model.keys():
            return self.model[tri_sentence]
        else:
            if self.smoothing:
                bi_sentence = ' '.join(tri_sentence.split(' ')[:2])
                if bi_sentence in self.bigram.keys():
                    return log(self.delta, 2) - log(self.bigram[bi_sentence] + self.delta * len(self.vocab()), 2)
                else:
                    return -log(len(self.vocab()), 2)
            else:
                return self.lbackoff

    def vocab(self):
        return self.unigram.keys()


class Bigram(LangModel):
    def __init__(self, backoff=0.001, delta=0.01, smoothing=True):
        self.model = dict()
        self.bigram = dict()
        self.unigram = dict()
        self.delta = delta
        self.smoothing = smoothing
        self.lbackoff = log(backoff, 2)

    def inc_bigram(self, b):
        if b in self.bigram:
            self.bigram[b] += 1.0
        else:
            self.bigram[b] = 1.0

    def inc_word(self, w):
        if w in self.unigram:
            self.unigram[w] += 1.0
        else:
            self.unigram[w] = 1.0

    def fit_sentence(self, sentence):
        sentence = ['*'] + sentence + ['END_OF_SENTENCE']
        bigram_list = [' '.join(sentence[i:i+2])
                       for i in range(len(sentence)-1)]

        for b in bigram_list:
            self.inc_bigram(b)

        for u in sentence:
            self.inc_word(u)
        self.inc_word('END_OF_SENTENCE')

    def norm(self):
        """Normalize and convert to log2-probs."""
        for b in self.bigram:
            u = b.split(' ')[0]
            if self.smoothing:
                self.model[b] = log(self.bigram[b]+self.delta, 2) - \
                    log(self.unigram[u]+self.delta *
                        len(self.unigram), 2)
            else:
                self.model[b] = log(self.bigram[b], 2) - \
                    log(self.unigram[b], 2)

    def cond_logprob(self, word, previous):
        bi_sentence = ''
        if not previous:
            bi_sentence = ' '.join(['*', word])
        else:
            bi_sentence = ' '.join([previous[-1], word])

        if bi_sentence in self.model:
            return self.model[bi_sentence]
        else:
            if self.smoothing:
                uni_sentence = bi_sentence.split(' ')[0]
                if uni_sentence in self.unigram:
                    return log(self.delta, 2) - log(self.unigram[uni_sentence] + self.delta * len(self.unigram), 2)
                else:
                    return -log(len(self.vocab()), 2)
            else:
                return self.lbackoff

    def vocab(self):
        return self.unigram.keys()
