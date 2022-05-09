# Assignment 4: Sequence Tagging

## How to Run

### 1. Single Rare Class

This process will do experiments for single rare class.

`python3 naive_replace_with_rare.py gene.train > gene_with_rare.train`

`python3 count_freqs.py gene_with_rare.train > gene.counts `

This will replace the rare words in the gene.train with \_RARE_ and then aggregate counts over the data.

#### 1.1 Base Line

`python3 naive_baseline_tagger.py gene.counts gene.dev > gene_dev.p1.out`

This will generate the results on dev set using the baseline model with single rare class.

#### 1. 2 Trigram HMM
`python3 naive_trigram_tagger.py gene.counts gene.dev > gene_dev.p1.out`

This will generate the results on dev set using the Trigram HMM model with single rare class.

### 2. Multiple Rare Classes

This process will do experiments for multiple rare classes.

`python3 improved_replace_with_rare.py gene.train > gene_with_rare.train`

`python3 count_freqs.py gene_with_rare.train > gene.counts `

This will replace the rare words in the gene.train with multiple rare classes and then aggregate counts over the data.

#### Base Line

`python3 improved_baseline_tagger.py gene.counts gene.dev > gene_dev.p1.out`

This will generate the results on dev set using the baseline model with multiple rare classes.

#### Trigram HMM

`python3 improved_trigram_tagger.py gene.counts gene.dev > gene_dev.p1.out`

This will generate the results on dev set using the Trigram HMM model with multiple rare classes.

#### Extension Trigram HMM

`python3 extension_trigram_tagger.py gene.counts gene.dev > gene_dev.p1.out`

This will generate the results on dev set using the Trigram HMM model with multiple rare classes and smoothing parameters.

### 3 Evaluate result

`python3 eval_gene_tagger.py gene.key gene_dev.p1.out `

This will evaluate the tagging result on the dev set.
