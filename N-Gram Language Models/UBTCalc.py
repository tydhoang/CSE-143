# @author Tyler Hoang
# CSE 143
# UBT.py program that finds the unigram, bigram, and trigram perplexity scores of the given file. Perplexity scores are outputted to a text file.
#

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

# Unigram perplexity calculation
def uniPerplexity(M, tokens, data):
	dataSetProbability = 0.0
	N = initializeN("Training_Token_Data.txt")
	for line in data:
		sentenceProbability = 0.0
		words = line.split()
		words.append("<STOP>")
		for word in words:
			wordProbability = Decimal(tokens[word])/Decimal(N)
			wordLogProb = math.log(wordProbability, 2)
			sentenceProbability = Decimal(sentenceProbability) + Decimal(wordLogProb)
		sentenceProbability = -sentenceProbability
		dataSetProbability = Decimal(dataSetProbability) + Decimal(sentenceProbability)
	preUniPerplexity = dataSetProbability/M
	uniPerplexity = 2**preUniPerplexity
	return uniPerplexity

# Bigram perplexity calculation
def biPerplexity(M, bigramFrequencies, unigramFrequencies, data):
	dataSetProbability = 0.0
	for line in data:
		sentenceProbability = 0.0
		words = line.split()
		words.insert(0, "<START>")
		words.append("<STOP>")
		for i in range(len(words)):
			if i + 1 == len(words):
				break
			bigram = (words[i], words[i + 1])
			if bigram in bigramFrequencies:
				bigramFrequency = bigramFrequencies[bigram]
				firstWordFrequency = unigramFrequencies[bigram[0]]
				bigramProbability = Decimal(bigramFrequency)/Decimal(firstWordFrequency)
				bigramLogProbability = math.log(bigramProbability, 2)
				sentenceProbability = Decimal(sentenceProbability) + Decimal(bigramLogProbability)
			else:
				return -1 # if there is a bigram that doesn't exist in the training data frequencies, the perplexity is infinite
		sentenceProbability = -sentenceProbability
		dataSetProbability = Decimal(dataSetProbability) + Decimal(sentenceProbability)
	preBiPerplexity = dataSetProbability/M
	biPerplexity = 2**preBiPerplexity
	return biPerplexity

# Trigram perplexity calculation
def triPerplexity(M, trigramFrequencies, bigramFrequencies, unigramFrequencies, data):
	dataSetProbability = 0.0
	for line in data:
		firstWord = True
		sentenceProbability = 0.0
		words = line.split()
		words.insert(0, "<START>")
		words.append("<STOP>")
		for i in range(len(words)):
			if i + 2 == len(words):
				break
			trigram = (words[i], words[i + 1], words[i + 2])

			if firstWord == True: # the first word of a sentence is treated differently. The bigram data is used due to the fact that there is no trigram that exists
				bigram = (words[i], words[i + 1])
				if bigram in bigramFrequencies:
					bigramFrequency = bigramFrequencies[bigram]
					firstWordFrequency = unigramFrequencies[bigram[0]]
					bigramProbability = Decimal(bigramFrequency)/Decimal(firstWordFrequency)
					bigramLogProbability = math.log(bigramProbability, 2)
					sentenceProbability = Decimal(sentenceProbability) + Decimal(bigramLogProbability)
					firstWord = False
				else:
					return -1 # if this bigram doesn't exist in the training data frequencies, the perplexity is infinite

			elif trigram in trigramFrequencies:
				bigram = (trigram[0], trigram[1])
				trigramFrequency = trigramFrequencies[trigram]
				bigramFrequency = bigramFrequencies[bigram]
				trigramProbability = Decimal(trigramFrequency)/Decimal(bigramFrequency)
				trigramLogProbability = math.log(trigramProbability, 2)
				sentenceProbability = Decimal(sentenceProbability) + Decimal(trigramLogProbability)
			else:
				return -1 # if there is a trigram that doesn't exist in the training data frequencies, the perplexity is infinite
		sentenceProbability = -sentenceProbability
		dataSetProbability = Decimal(dataSetProbability) + Decimal(sentenceProbability)
	preTriPerplexity = dataSetProbability/M
	triPerplexity = 2**preTriPerplexity
	return triPerplexity

def main():
    trainingTokens = initializeFrequencies({},"Training_Token_Data.txt")
    bigramFrequencies = initializeFrequencies({}, "Training_Bigram_data.txt")
    trigramFrequencies = initializeFrequencies({}, "Training_Trigram_data.txt")
    M = 0
    data = open(sys.argv[1])
    for line in data:
        words = line.split()
        words.append("<STOP>")
        M += len(words)

    inputFile = open(sys.argv[1])
    UniPerplexity = uniPerplexity(M, trainingTokens, inputFile)
    inputFile.close()
    inputFile = open(sys.argv[1])
    BiPerplexity = biPerplexity(M, bigramFrequencies, trainingTokens, inputFile)
    inputFile.close()
    inputFile = open(sys.argv[1])
    TriPerplexity = triPerplexity(M, trigramFrequencies, bigramFrequencies, trainingTokens, inputFile)

    outfile = open("UBT.txt", "w")
    outfile.write("Unigram perplexity: " + str(UniPerplexity) + "\n")
    if BiPerplexity == -1:
        outfile.write("Bigram perplexity: positive infinity\n")
    else:
        outfile.write("Bigram perplexity: " + str(BiPerplexity) + "\n")
    if TriPerplexity == -1:
        outfile.write("Trigram perplexity: positive infinity\n")
    else:
        outfile.write("Trigram perplexity: " + str(TriPerplexity) + "\n")
main()