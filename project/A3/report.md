# Assignment 3: Language Modeling

## 1. Unigram Language Model Analysis

### 1.1. Analysis on In-Domain Text

![download](/Users/leyang/Desktop/courses/download.png)

In this part,  we divide the amount into 10 different size of training data chunks in each of the three domains. Then we train a unigram language model for each of the domains, calculate the perplexity on different training data size and plot the result.

From the above graph, we can see how perplexity changes as mount of training data varied in each of the three domains. On Reuters corpus and Brown corpus, we can see that when the training data size becomes larger and larger, the perplexity becomes smaller and smaller. I think this is because when the training data size increase, there can be more sentences fitted in the model, and the model's performance increases. However, we can see that on Gutenberg Corpus, as the training data size increase, the perplexity first goes down, but when the size is larger than 40000, the perplexity goes up. I think this is because of the unusual distribution of the data of Gutenberg  Corpus. The words closer to the front fits the model of the whole dataset better. While words closer to the back is not very common.

