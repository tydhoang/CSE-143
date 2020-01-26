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

def biPerplexity(N, bigramFrequencies, unigramFrequencies, data):
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
	preBiPerplexity = dataSetProbability/N
	biPerplexity = 2**preBiPerplexity
	return biPerplexity

def main():
	unigramFrequencies = initializeFrequencies({}, "Training_Token_Data.txt")
	bigramFrequencies = initializeFrequencies({},"Training_Bigram_Data.txt")
	NTraining = initializeN("Training_Token_Data.txt")
	training = open("1b_benchmark.train.tokens")
	trainingBiPerplexity = biPerplexity(NTraining, bigramFrequencies, unigramFrequencies, training)

	NTest = initializeN("Test_Token_Data.txt")
	test = open("1b_benchmark.test.tokens")
	testBiPerplexity = biPerplexity(NTest, bigramFrequencies, unigramFrequencies, test)

	NDev = initializeN("Dev_Token_Data.txt")
	dev = open("1b_benchmark.dev.tokens")
	devBiPerplexity = biPerplexity(NDev, bigramFrequencies, unigramFrequencies, dev)

	outfile = open("Bigram_Perplexities_ALL.txt", "w")
	if trainingBiPerplexity == -1:
		outfile.write("Training data bigram perplexity: positive infinity\n")
	else:
		outfile.write("Training data bigram perplexity: " + str(trainingBiPerplexity) + "\n")
	if testBiPerplexity == -1:
		outfile.write("Test data bigram perplexity: positive infinity\n")
	else:
		outfile.write("Test data bigram perplexity: " + str(testBiPerplexity) + "\n")
	if devBiPerplexity == -1:
		outfile.write("Dev data bigram perplexity: positive infinity\n")
	else:
		outfile.write("Dev data bigram perplexity: " + str(devBiPerplexity))

main()