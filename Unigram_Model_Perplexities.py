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

def uniPerplexity(N, tokens, data):
	dataSetProbability = 0.0
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
	preUniPerplexity = dataSetProbability/N
	uniPerplexity = 2**preUniPerplexity
	return uniPerplexity

def main():
	trainingTokens = initializeFrequencies({},"Training_Token_Data.txt")
	NTraining = initializeN("Training_Token_Data.txt")
	training = open("1b_benchmark.train.tokens")
	trainingUniPerplexity = uniPerplexity(NTraining, trainingTokens, training)

	testTokens = initializeFrequencies({},"Test_Token_Data.txt")
	NTest = initializeN("Test_Token_Data.txt")
	test = open("1b_benchmark.test.tokens")
	testUniPerplexity = uniPerplexity(NTest, testTokens, test)

	devTokens = initializeFrequencies({},"Dev_Token_Data.txt")
	NDev = initializeN("Dev_Token_Data.txt")
	dev = open("1b_benchmark.dev.tokens")
	devUniPerplexity = uniPerplexity(NDev, devTokens, dev)

	outfile = open("Unigram_Perplexities_ALL.txt", "w")
	outfile.write("Training data unigram perplexity: " + str(trainingUniPerplexity) + "\n")
	outfile.write("Test data unigram perplexity: " + str(testUniPerplexity) + "\n")
	outfile.write("Dev data unigram perplexity: " + str(devUniPerplexity))

main()