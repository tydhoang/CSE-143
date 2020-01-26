#! /usr/bin/env python3
import fileinput
import sys
import math
from decimal import Decimal

def initializeFrequencies(tokens, file):
	tokens = {}
	tokenData = open(file)
	next(tokenData)
	for line in tokenData:
		tokens = eval(line)
	return tokens

def initializeN(file):
	data = open(file)
	N = int(data.readline())
	return N

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
				return -1
		sentenceProbability = -sentenceProbability
		dataSetProbability = Decimal(dataSetProbability) + Decimal(sentenceProbability)
	preBiPerplexity = dataSetProbability/M
	biPerplexity = 2**preBiPerplexity
	return biPerplexity

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

			if firstWord == True:
				bigram = (words[i], words[i + 1])
				if bigram in bigramFrequencies:
					bigramFrequency = bigramFrequencies[bigram]
					firstWordFrequency = unigramFrequencies[bigram[0]]
					bigramProbability = Decimal(bigramFrequency)/Decimal(firstWordFrequency)
					bigramLogProbability = math.log(bigramProbability, 2)
					sentenceProbability = Decimal(sentenceProbability) + Decimal(bigramLogProbability)
					firstWord = False
				else:
					return -1

			elif trigram in trigramFrequencies:
				bigram = (trigram[0], trigram[1])
				trigramFrequency = trigramFrequencies[trigram]
				bigramFrequency = bigramFrequencies[bigram]
				trigramProbability = Decimal(trigramFrequency)/Decimal(bigramFrequency)
				trigramLogProbability = math.log(trigramProbability, 2)
				sentenceProbability = Decimal(sentenceProbability) + Decimal(trigramLogProbability)
			else:
				return -1
		sentenceProbability = -sentenceProbability
		dataSetProbability = Decimal(dataSetProbability) + Decimal(sentenceProbability)
	preTriPerplexity = dataSetProbability/M
	triPerplexity = 2**preTriPerplexity
	return triPerplexity

def main():
    trainingTokens = initializeFrequencies({},"Training_Token_Data.txt")
    bigramFrequencies = initializeFrequencies({}, "Training_Bigram_data.txt")
    trigramFrequencies = initializeFrequencies({}, "Training_Trigram_data.txt")
    NTraining = initializeN("Training_Token_Data.txt")
    training = open("1b_benchmark.train.tokens")
    trainingUniPerplexity = uniPerplexity(NTraining, trainingTokens, training)
    training.close()
    training = open("1b_benchmark.train.tokens")
    trainingBiPerplexity = biPerplexity(NTraining, bigramFrequencies, trainingTokens, training)
    training.close()
    training = open("1b_benchmark.train.tokens")
    trainingTriPerplexity = triPerplexity(NTraining, trigramFrequencies, bigramFrequencies, trainingTokens, training)

    outfile = open("Training_ALL_UBT.txt", "w")
    outfile.write("Training data unigram perplexity: " + str(trainingUniPerplexity) + "\n")
    if trainingBiPerplexity == -1:
        outfile.write("Training data bigram perplexity: positive infinity\n")
    else:
        outfile.write("Training data bigram perplexity: " + str(trainingBiPerplexity) + "\n")
    if trainingTriPerplexity == -1:
        outfile.write("Training data trigram perplexity: positive infinity\n")
    else:
        outfile.write("Training data trigram perplexity: " + str(trainingTriPerplexity) + "\n")
main()