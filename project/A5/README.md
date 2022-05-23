# Assignment 5: Machine Translation

## How to Run

1. `python3 ibm1.py`: this will train IBM Model 1, then generate `dev.out` for evaluating and `ibm1.model` for t parameter for IBM Model 2
2. `python3 eval_alignment.py dev.key dev.out`:this will evaluate the alignment result from IBM Model 1
3. `python3 ibm2.py`: this will train IBM Model 2, then generate `dev.out` for evaluating 
4. `python3 eval_alignment.py dev.key dev.out`:this will evaluate the alignment result from IBM Model 2

