import pickle


class IBM1:
    def __init__(self, en_corpus, es_corpus):
        self.t_parameter = {}
        self.read_corpus_addnull(en_corpus, es_corpus)
        self.n_e = {}
        parallel_corpus = zip(self.english, self.spanish)
        wordpairs = set()
        for e, s in parallel_corpus:
            for e_j in e:
                for s_i in s:
                    wordpair = (e_j, s_i)
                    if wordpair not in wordpairs:
                        wordpairs.add(wordpair)
                        if not e_j in self.n_e:
                            self.n_e[e_j] = 0
                        self.n_e[e_j] += 1

    def read_corpus_addnull(self, en_corpus, es_corpus):
        self.english = [["*"] + e_sent.split() for e_sent in open(en_corpus)]
        self.spanish = [f_sent.split() for f_sent in open(es_corpus)]

    def read_dev_addnull(self, en_dev, es_dev):
        self.english_dev = [["*"] + e_sent.split() for e_sent in open(en_dev)]
        self.spanish_dev = [f_sent.split() for f_sent in open(es_dev)]

    def em_algorithm(self, iterations=5):
        for i in range(iterations):
            print('iter: ' + str(i))
            c_e_f_dict = {}
            c_e_dict = {}
            parallel_corpus = zip(self.english, self.spanish)
            for e, s in parallel_corpus:
                for s_i in s:
                    sum_t = self.get_sum_t(s_i, e)
                    for e_j in e:
                        t = self.t_parameter.get((s_i, e_j), 1.0/self.n_e[e_j])
                        delta = float(t)/sum_t
                        c_e_f_dict[(e_j, s_i)] = c_e_f_dict.get(
                            (e_j, s_i), 0.0) + delta
                        c_e_dict[e_j] = c_e_dict.get(e_j, 0.0) + delta

            for (e_j, s_i), ej_si_score in c_e_f_dict.items():
                self.t_parameter[(s_i, e_j)] = float(
                    ej_si_score) / c_e_dict[e_j]

    def get_sum_t(self, s_i, e):
        sum_t = 0.0
        for e_j in e:
            sum_t += self.t_parameter.get((s_i, e_j), 1.0/self.n_e[e_j])
        return sum_t

    def save_parameter(self, save_path='ibm1.model'):
        with open(save_path, 'wb') as save_file:
            pickle.dump(self.t_parameter, save_file)

    def alignment(self, en_dev='dev.en', es_dev='dev.es', out_path='dev.out'):
        self.read_dev_addnull(en_dev, es_dev)
        parallel_dev = zip(self.english_dev, self.spanish_dev)
        with open(out_path, 'w') as out_file:
            line = 1
            for e, s in parallel_dev:
                result = self.get_result(e, s)
                count = 1
                for i in result:
                    out_file.write('%d %d %d\r\n' % (line, i, count))
                    count += 1
                line += 1

    def get_result(self, e, s):
        result = []
        for i in range(len(s)):
            max_j = 0
            max_t = 0
            for j in range(len(e)):
                e_j, s_i = e[j], s[i]
                t = self.t_parameter.get((s_i, e_j), 0)
                if t > max_t:
                    max_j, max_t = j, t
            result.append(max_j)
        return result


if __name__ == '__main__':
    ibm1 = IBM1(en_corpus='corpus.en', es_corpus='corpus.es')
    ibm1.em_algorithm(iterations=5)
    ibm1.save_parameter()
    ibm1.alignment()
