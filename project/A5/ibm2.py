import pickle


class IBM2:
    def __init__(self, ibm1, en_corpus, es_corpus):
        self.q_parameter = {}
        with open(ibm1, 'rb') as ibm1_file:
            self.t_parameter = pickle.load(ibm1_file)
        self.read_corpus_addnull(en_corpus, es_corpus)

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
            c_j_i_l_m_dict = {}
            c_i_l_m_dict = {}

            parallel_corpus = zip(self.english, self.spanish)
            for e, s in parallel_corpus:
                l = len(s)
                m = len(e)
                for i in range(len(s)):
                    sum_q_t = self.get_sum_q_t(s, e, l, m, i)
                    for j in range(len(e)):
                        q_t = self.q_parameter.get(
                            (j, i, l, m), 1.0/(l+1))*self.t_parameter[(s[i], e[j])]
                        delta = float(q_t)/sum_q_t
                        c_e_f_dict[(e[j], s[i])] = c_e_f_dict.get(
                            (e[j], s[i]), 0.0) + delta
                        c_e_dict[e[j]] = c_e_dict.get(e[j], 0.0) + delta
                        c_j_i_l_m_dict[(j, i, l, m)] = c_j_i_l_m_dict.get(
                            (j, i, l, m), 0.0)+delta
                        c_i_l_m_dict[(i, l, m)] = c_i_l_m_dict.get(
                            (i, l, m), 0.0) + delta

            for (e_j, s_i), ej_si_score in c_e_f_dict.items():
                self.t_parameter[(s_i, e_j)] = float(
                    ej_si_score) / c_e_dict[e_j]
            for (j, i, l, m), j_i_l_m_score in c_j_i_l_m_dict.items():
                self.q_parameter[(j, i, l, m)] = float(
                    j_i_l_m_score)/c_i_l_m_dict[(i, l, m)]

    def get_sum_q_t(self, s, e, l, m, i):
        sum_q_t = 0.0
        for j in range(len(e)):
            sum_q_t += self.t_parameter[(s[i], e[j])] * \
                self.q_parameter.get((j, i, l, m), 1.0/(l+1))
        return sum_q_t

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
        l = len(s)
        m = len(e)
        for i in range(len(s)):
            max_j = 0
            max_q_t = 0
            for j in range(len(e)):
                e_j, s_i = e[j], s[i]
                q_t = self.t_parameter.get(
                    (s_i, e_j), 0)*self.q_parameter.get((j, i, l, m), 0)

                if q_t > max_q_t:
                    max_j, max_q_t = j, q_t
            result.append(max_j)
        return result


if __name__ == '__main__':
    ibm2 = IBM2(ibm1='ibm1.model', en_corpus='corpus.en',
                es_corpus='corpus.es')
    ibm2.em_algorithm(iterations=5)
    ibm2.alignment()
