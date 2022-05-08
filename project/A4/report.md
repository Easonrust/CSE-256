# Assignment 4: Sequence Tagging

## 1. Baseline

### 1.1 Rare Classes Design

We group rare/unseen words into classes to improve the baseline model. The potential choices are as follows:

1. \_RARE\_ALNUM\_ and \_RARE_PUNCT\_: We can group the words into words that only contain alphabetic and numeric characters and words that contain no alphabetic and numeric characters and words which are mostly punctuation characters.
2. \_RARE\_AL\_, \_RARE\_NUM\_  and \_RARE_PUNCT\_: We can group the words into words that only contain alphabetic characters, words that only contain numeric characters and words that contain no alphabetic and numeric characters and words which are mostly punctuation characters.
3. \_RARE\_ALUP\_, \_RARE\_ALLOW\_, \_RARE\_NUM\_  and \_RARE_PUNCT\_: We can group the words into words that only contain uppercase alphabetic characters, words that only contain lowercase alphabetic characters, words that only contain numeric characters and words that contain no alphabetic and numeric characters and words which are mostly punctuation characters.

The results for the three choices on the dev sets are as follows:

|                                                              | Precision | Recall   | F1-Score |
| ------------------------------------------------------------ | --------- | -------- | -------- |
| **\(_RARE\_ALNUM\_ ,  \_RARE_PUNCT\_)**                      | 0.158505  | 0.652648 | 0.255653 |
| **(\_RARE\_AL\_, \_RARE\_NUM\_, \_RARE_PUNCT\_)**            | 0.158292  | 0.652648 | 0.254789 |
| **\(_RARE\_ALUP\_, \_RARE\_ALLOW\_, \_RARE\_NUM\_, \_RARE_PUNCT\_)** | 0.178760  | 0.579439 | 0.273228 |

We find that in the third choice we can get the best F1-Score at 0.273228, therefore we choose **\(_RARE\_ALUP\_, \_RARE\_ALLOW\_, \_RARE\_NUM\_, \_RARE_PUNCT\_)** method.

### 1.2 Results

Dev

Found 2081 GENEs. Expected 642 GENEs; Correct: 372.



​	 precision 	recall 		F1-Score

GENE:	 0.178760	0.579439	0.273228
