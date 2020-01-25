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

def smooth(unigramTokens, bigramTokens, trigramTokens, weight1, weight2, weight3, N, fileName):
	data = open(fileName)
	dataSetProb = 0.0
	for line in data:
		firstWord = True
		sentenceProb = 0.0
		words = line.split()
		words.insert(0, "<START>")
		words.append("<STOP>")
		for i in range(len(words)):
			if i == 0:
				continue
			if firstWord == True:
				unigram = words[i]
				bigram = (words[i - 1], words[i])
				trigram = bigram
			else:
				unigram = words[i]
				bigram = (words[i - 1], words[i])
				trigram = (words[i - 2], words[i - 1], words[i])

			unigramProb = Decimal(unigramTokens[unigram])/Decimal(N)
			bigramProb = Decimal(bigramTokens[bigram])/Decimal(unigramTokens[bigram[0]])
			if firstWord == True:
				trigramProb = 1
				firstWord = False
			else:
				triBigram = (trigram[0], trigram[1])
				trigramProb = Decimal(trigramTokens[trigram])/Decimal(bigramTokens[triBigram])
			SmoothedProb = Decimal(weight1)*unigramProb + Decimal(weight2)*bigramProb + Decimal(weight3)*trigramProb
			SmoothedProb = math.log(SmoothedProb, 2)
			sentenceProb = Decimal(sentenceProb) + Decimal(SmoothedProb)
		sentenceProb = -sentenceProb
		dataSetProb = Decimal(dataSetProb) + Decimal(sentenceProb)
	dataSetProb = dataSetProb/N
	perplexity = 2**dataSetProb
	return perplexity


def main():
	unigramTokens = initializeFrequencies({}, "Dev_Token_Data.txt")
	bigramTokens = initializeFrequencies({}, "Dev_Bigram_Data.txt")
	trigramTokens = initializeFrequencies({}, "Dev_Trigram_Data.txt")

	data = open("Dev_Trigram_Data.txt")
	N = int(data.readline())
	data.close()

	weight1 = Decimal(input("Enter unigram weight: "))
	weight2 = Decimal(input("Enter bigram weight: "))
	weight3 = Decimal(input("Enter trigram weight: "))

	p = smooth(unigramTokens, bigramTokens, trigramTokens, weight1, weight2, weight3, N, "1b_benchmark.dev.tokens")
	outfile = open("Smoothing_Hyperparamters.txt", "w")
	outfile.write("The following hyperparameters were used: \n")
	outfile.write("Unigram Weight: " + str(weight1) + "\n")
	outfile.write("Bigram Weight: " + str(weight2) + "\n")
	outfile.write("Trigram Weight: " + str(weight3) + "\n")
	outfile.write("Smoothed Perplexity: " + str(p))


main()