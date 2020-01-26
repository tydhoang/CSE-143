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
    NDev = initializeN("Dev_Token_Data.txt")
    dev = open("1b_benchmark.dev.tokens")
    devUniPerplexity = uniPerplexity(NDev, trainingTokens, dev)
    dev.close()
    dev = open("1b_benchmark.dev.tokens")
    devBiPerplexity = biPerplexity(NDev, bigramFrequencies, trainingTokens, dev)
    dev.close()
    dev = open("1b_benchmark.dev.tokens")
    devTriPerplexity = triPerplexity(NDev, trigramFrequencies, bigramFrequencies, trainingTokens, dev)

    outfile = open("Dev_ALL_UBT.txt", "w")
    outfile.write("Dev data unigram perplexity: " + str(devUniPerplexity) + "\n")
    if devBiPerplexity == -1:
        outfile.write("Dev data bigram perplexity: positive infinity\n")
    else:
        outfile.write("Dev data bigram perplexity: " + str(devBiPerplexity) + "\n")
    if devTriPerplexity == -1:
        outfile.write("Dev data trigram perplexity: positive infinity\n")
    else:
        outfile.write("Dev data trigram perplexity: " + str(devTriPerplexity) + "\n")
main()