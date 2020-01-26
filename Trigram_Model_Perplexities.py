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

def triPerplexity(N, trigramFrequencies, bigramFrequencies, data):
	dataSetProbability = 0.0
	for line in data:
		sentenceProbability = 0.0
		words = line.split()
		words.insert(0, "<START>")
		words.append("<STOP>")
		for i in range(len(words)):
			if i + 2 == len(words):
				break
			trigram = (words[i], words[i + 1], words[i + 2])
			if trigram in trigramFrequencies:
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
	preTriPerplexity = dataSetProbability/N
	triPerplexity = 2**preTriPerplexity
	return triPerplexity

def main():
	bigramFrequencies = initializeFrequencies({}, "Training_Bigram_Data.txt")
	trigramFrequencies = initializeFrequencies({},"Training_Trigram_Data.txt")
	NTraining = initializeN("Training_Token_Data.txt")
	training = open("1b_benchmark.train.tokens")
	trainingTriPerplexity = triPerplexity(NTraining, trigramFrequencies, bigramFrequencies, training)

	NTest = initializeN("Test_Token_Data.txt")
	test = open("1b_benchmark.test.tokens")
	testTriPerplexity = triPerplexity(NTest, trigramFrequencies, bigramFrequencies, test)

	NDev = initializeN("Dev_Token_Data.txt")
	dev = open("1b_benchmark.dev.tokens")
	devTriPerplexity = triPerplexity(NDev, trigramFrequencies, bigramFrequencies, dev)

	outfile = open("Trigram_Perplexities_ALL.txt", "w")
	if trainingTriPerplexity == -1:
		outfile.write("Training data trigram perplexity: positive infinity\n")
	else:
		outfile.write("Training data trigram perplexity: " + str(trainingTriPerplexity) + "\n")
	if testTriPerplexity == -1:
		outfile.write("Test data trigram perplexity: positive infinity\n")
	else:
		outfile.write("Test data trigram perplexity: " + str(testTriPerplexity) + "\n")
	if devTriPerplexity == -1:
		outfile.write("Dev data trigram perplexity: positive infinity\n")
	else:
		outfile.write("Dev data trigram perplexity: " + str(devTriPerplexity))


main()