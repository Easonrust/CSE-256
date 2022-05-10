# Assignment 4: Sequence Tagging

## Baseline

### Rare Classes Design

We group rare/unseen words into classes to improve the baseline model. The potential choices are as follows:

1. \_RARE\_: There are only one class.
1. \_RARE\_ALNUM\_ and \_RARE_PUNCT\_: We can group the words into words that only contain alphabetic and numeric characters and words that contain no alphabetic and numeric characters and words which are mostly punctuation characters.
2. \_RARE\_AL\_, \_RARE\_NUM\_  and \_RARE_PUNCT\_: We can group the words into words that only contain alphabetic characters, words that only contain numeric characters and words that contain no alphabetic and numeric characters and words which are mostly punctuation characters.
3. \_RARE\_ALUP\_, \_RARE\_ALLOW\_, \_RARE\_NUM\_  and \_RARE_PUNCT\_: We can group the words into words that only contain uppercase alphabetic characters, words that only contain lowercase alphabetic characters, words that only contain numeric characters and words that contain no alphabetic and numeric characters and words which are mostly punctuation characters.

The results for the three choices on the dev sets are as follows:

|                                                              | Precision | Recall   | F1-Score |
| ------------------------------------------------------------ | --------- | -------- | -------- |
| **\(_RARE\_)**                                               | 0.158861  | 0.660436 | 0.256116 |
| **\(_RARE\_ALNUM\_ ,  \_RARE_PUNCT\_)**                      | 0.158505  | 0.652648 | 0.255653 |
| **(\_RARE\_AL\_, \_RARE\_NUM\_, \_RARE_PUNCT\_)**            | 0.158292  | 0.652648 | 0.254789 |
| **\(_RARE\_ALUP\_, \_RARE\_ALLOW\_, \_RARE\_NUM\_, \_RARE_PUNCT\_)** | 0.178760  | 0.579439 | 0.273228 |

We find that in the fourth choice we can get the best F1-Score at 0.273228 on the dev set, therefore we choose **\(_RARE\_ALUP\_, \_RARE\_ALLOW\_, \_RARE\_NUM\_, \_RARE_PUNCT\_)** method.

### Results

Therefore, we can get the result on the dev set using the new baseline model. The number expected GENEs  is 642, the number of found GENEs is 2081, and the number of correct ones is 372.

| Precision | Recall   | F1-Score |
| --------- | -------- | -------- |
| 0.178760  | 0.579439 | 0.273228 |

Compared to the naive baseline model where we only use single rare class and get F1-Score at 0.256116, I think the reason for this that the new baseline model make the rare and unseen words more informative.
## Trigram HMM

### The Purpose of the Viterbi Algorithm

In this situation we need to solve the sequence tagging problem: let $S$ be the potential tag set ${0, I-GENE}$, giving an sentence($x_1,...x_n$) as input, we are going to find that $(y_1...y_{n+1})$, where $y_{n+1}=STOP$ , $y_i \in S$, then:
$$
arg\ max_{y_1...y_{n+1}}p(x_1...x_n, y_1 ... y_{n+1}) \\
p(x_1...x_n, y_1 ... y_{n+1})=\prod_{i=1}^{n+1} q(y_i|y_{i-2},y_{i-1})\prod_{i=1}^{n}e(x_i|y_i)
$$
The Viterbi algorithm is a dynamic programming algorithm for obtaining the maximum a posteriori probability estimate of the most likely sequence of hidden states, which are called the Viterbi path, that results in a sequence of observed events. In this case, given the sequence of observations, we can use the Viterbi Algorithm to find the most likely corresponding sequence of hidden states and it can solve the above problem recursively.

Let $n$ represent the length of the input, and $|S|$ is the length of the tag set. Let's compare the Viterbi algorithm(dynamic programming) with brute force and greedy method.

Using Viterbi algorithm, we need to calculate $n|S|^2$  entries in the dynamic programm table(which is defined in the following section), and it take us $O(|S|)$ time to calculate each entry. Therefore the time complexity for Viterbi Algorithm is $O(n|S|^3)$.

Using brute force method, it take us $O(|S|)$ time to tag each word, and the time complexity is $O(|S|^n)$, which is too bard.

Using the greedy method, the tagger will greedily choose the best tag for each word and then move on to next one, but in this case we can not performs a global optimisation and guarantees to find the most likely state sequence by exploring all possible state sequences.

Thus in this case, we use Viterbi algorithm to solve the problem.



### Specifics of Implementation

When implementing the Viterbi algorithm, we let $y_0=y_1=*$, and $y_{n+1}=STOP$. Let $S_{-1}=S_0=\{*\}$ and $S_k=S\ for \ k \in{1...n}$. Then we using the dynamic programming table $\pi(k,u,v)$ to represent the maximum probability of a tag sequence ending in tags $u,v$ at position $k$ given the input. Then we show how to compute $\pi(k,u,v)$ and the process of the algorithm:

1. In the base case, $\pi(0,*,*)=1$

2. For any $k\in\{1...n\}$, $u\in S_{k-1}$ and $v\in S_k$, we have:
   $$
   \pi(k,u,v) = max_{w\in S_{k-2}}(\pi(k-1,w,u)\times q(v|w,u)\times e(x_k|v))
   $$
   Using backpointers method, we can use $bp(k,u,v)$ to store $w$ that $bp(k,u,v)=arg \ max_{w\in S_{k-2}}(\pi(k-1,w,u)\times q(v|w,u)\times e(x_k|v))$.
   
3. The last two tags $(y_{n-1},y_n)=arg \ max_{(u,v)}(\pi(n,u,v)\times q(STOP|u,v))$, For any $k=(n-2)...1$, $y_k=bp(k+2,y_{k+1},y_{k+2})$.

4. Then we can get the tag sequence $y_1,...,y_n$.

The pseudo code is as follows:

![image-20220508190251290](https://tva1.sinaimg.cn/large/e6c9d24egy1h21xarai21j210c0dodi3.jpg)

### Naive Trigram Hmm Model

In this case, we only replace the rare only unseen words with \_RARE\_, and then get the following result on the dev set.

| Precision | Recall   | F1-Score |
| --------- | -------- | -------- |
| 0.541555  | 0.314642 | 0.398030 |

The number expected GENEs  is 642, the number of found GENEs is 373, and the number of correct ones is 202. Compared to the results in section **1.1**, we find that the precision is higher than baseline, but the recall is a little lower, and the F1-Score is better than baseline, which means the result is much more accurate than base line model.

### Improved Trigram Model

In this section, we still design the rare word classes like the way we do in section **1.1**, and report the results on different models on dev sets, which are shown as below.

|                                                              | Precision | Recall   | F1-Score |
| ------------------------------------------------------------ | --------- | -------- | -------- |
| **\(_RARE\_)**                                               | 0.541555  | 0.314642 | 0.398030 |
| **\(_RARE\_ALNUM\_ ,  \_RARE_PUNCT\_)**                      | 0.543011  | 0.314642 | 0.398422 |
| **(\_RARE\_AL\_, \_RARE\_NUM\_, \_RARE_PUNCT\_)**            | 0.551220  | 0.352025 | 0.429658 |
| **\(_RARE\_ALUP\_, \_RARE\_ALLOW\_, \_RARE\_NUM\_, \_RARE_PUNCT\_)** | 0.512500  | 0.319315 | 0.393474 |

We find that in the third choice we can get the best F1-Score at 0.429658 on the dev set, therefore we choose **(\_RARE\_AL\_, \_RARE\_NUM\_, \_RARE_PUNCT\_)** method.

### Comparision based on Results

Comparing the results we got from the trigram model and the baseline model, we can find that using Viterbi algorithm and trigram model we can get more accurate results, which means our precision is high. However, our recall is a little low, but combining with the high precision we can get a higher F1-Score.

Comparing the results we got from the model with single rare class and multiple rare class, we can find that  for baseline model, grouping words into informative word classes can improve precision; for trigram modelm grouping words into informative word classes can improve precision and recall, thus improve the F1-Score.



## Extensions

In this section, we make an extension to the trigram HMM tagger. We using the add-$\delta$ Method to smooth the emission parameters, thus the function that computes emission parameters is:
$$
e(x|y)=\frac{Count(y \rightsquigarrow x)+\delta}{Count(y)+|S|*\delta}
$$
Where $|S|$ is the length of the tag set, we still choose the **(\_RARE\_AL\_, \_RARE\_NUM\_, \_RARE_PUNCT\_)** method, and find that when we set $\delta=0.2$, we can get better result then section **2**, which is as follows:

| Precision | Recall   | F1-Score |
| --------- | -------- | -------- |
| 0.555012  | 0.353583 | 0.431970 |

We find that the result F1-Score is 0.431970, which is better than the best result 0.429658 we get before.

We think the reason for this is that smoothing parameters can ensure the emission parameter can output a non-zero and valid probability distribution for out-of-vocabulary words as well, thus it can improve the result.