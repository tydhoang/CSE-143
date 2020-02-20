# @author Tyler Hoang
# CSE 143
# Smoothing.py program that essentially combines all 3 language models into 1 using hyperparameters. Asks for hyperparameter inputs and outputs the perplexity score
# to Smoothed_Final.txt

#! /usr/bin/env python3
import fileinput
import sys
import math
from decimal import Decimal

# Used for reading in the training unigram/bigram/trigram data for frequency data
def initializeFrequencies(tokens, file):
	tokens = {}
	tokenData = open(file)
	next(tokenData)
	for line in tokenData:
		tokens = eval(line)
	return tokens

# Used to attain the N from the training data
def initializeN(file):
	data = open(file)
	N = int(data.readline())
	return N

# Take the unigram, bigram, and trigram probabilities and sum them using the given weights
def smooth(unigramTokens, bigramTokens, trigramTokens, weight1, weight2, weight3, M, fileName):
	data = open(fileName)
	N = initializeN("Training_Token_Data.txt")
	dataSetProb = 0.0
	for line in data:
		firstWord = True
		sentenceProb = 0.0
		words = line.split()
		words.insert(0, "<START>")
		words.append("<STOP>")
		for i in range(len(words)):
			if i == 0: #Skip the <START> token
				continue
			if firstWord == True: # The trigram for the first word is a bigram
				unigram = words[i]
				bigram = (words[i - 1], words[i])
				trigram = bigram
			else:
				unigram = words[i]
				bigram = (words[i - 1], words[i])
				trigram = (words[i - 2], words[i - 1], words[i])

			if firstWord == True:
				unigramProb = Decimal(unigramTokens[unigram])/Decimal(N)
				isBigram = bigramTokens.get(bigram)
				if isBigram == None:
					bigramProb = 0
				else:
					bigramProb = Decimal(bigramTokens[bigram])/Decimal(unigramTokens[bigram[0]])
				trigramProb = bigramProb
				firstWord = False
			
			else:
				unigramProb = Decimal(unigramTokens[unigram])/Decimal(N)
				isBigram = bigramTokens.get(bigram)
				if isBigram == None:
					bigramProb = 0
				else:
					bigramProb = Decimal(bigramTokens[bigram])/Decimal(unigramTokens[bigram[0]])
				isTrigram = trigramTokens.get(trigram)
				if isTrigram == None:
					trigramProb = 0
				else:
					triBigram = (trigram[0], trigram[1])
					trigramProb = Decimal(trigramTokens[trigram])/Decimal(bigramTokens[triBigram])
			SmoothedProb = Decimal(weight1)*unigramProb + Decimal(weight2)*bigramProb + Decimal(weight3)*trigramProb
			SmoothedProb = math.log(SmoothedProb, 2)
			sentenceProb = Decimal(sentenceProb) + Decimal(SmoothedProb)
		sentenceProb = -sentenceProb
		dataSetProb = Decimal(dataSetProb) + Decimal(sentenceProb)
	dataSetProb = dataSetProb/M
	perplexity = 2**dataSetProb
	return perplexity


def main():
    unigramTokens = initializeFrequencies({}, "Training_Token_Data.txt")
    bigramTokens = initializeFrequencies({}, "Training_Bigram_Data.txt")
    trigramTokens = initializeFrequencies({}, "Training_Trigram_Data.txt")
    M = 0
    data = open(sys.argv[1])
    for line in data:
        words = line.split()
        words.append("<STOP>")
        M += len(words)

    weight1 = Decimal(input("Enter unigram weight: "))
    weight2 = Decimal(input("Enter bigram weight: "))
    weight3 = Decimal(input("Enter trigram weight: "))

    p = smooth(unigramTokens, bigramTokens, trigramTokens, weight1, weight2, weight3, M, sys.argv[1])
    outfile = open("Smoothed_Final.txt", "w")
    outfile.write("The following hyperparameters were used: \n")
    outfile.write("Unigram Weight: " + str(weight1) + "\n")
    outfile.write("Bigram Weight: " + str(weight2) + "\n")
    outfile.write("Trigram Weight: " + str(weight3) + "\n")
    outfile.write("Smoothed Perplexity: " + str(p))


main()