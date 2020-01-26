Tyler Hoang
CSE 143
A1

Included Files:
Training_Token_Initialization.py
UBTCalc.py
Smoothing.py

Instructions:
Programs must be run in a specific order!

1. Run Training_Token_Initialization.py. This will create <UNK> tokens and create the dictionaries necessary for perplexity calculation. This program outputs this information to the files Training_Token_Data.txt, Training_Bigram_Data.txt, and Training_Trigram_Data.txt.

2. Run UBTCalc.py on the desired data set:
For example: 

	python3 UBTCalc.py 1b_benchmark.train.tokens

This produces the output file UBT.txt, which contains the unigram, bigram, and trigram perplexity scores for the training data set. This can be run on the dev and test data sets as well (or any other data set).

3. Run Smoothing.py on the desired data set:
For example:

	python3 Smoothing.py 1b_benchmark.dev.tokens

This runs the linear interpolated model on the dev data set. The program asks the user for weight input, so type in the respective weights when prompted. The results are outputted to the file Smoothing_Final.txt

Note: The programs do take a while to run so do be patient.