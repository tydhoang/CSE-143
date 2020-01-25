#! /usr/bin/env python3
import fileinput
import sys

def main():
	N = 0
	trainingTokens = {}
	bigramTokens = {}
	trigramTokens = {}

	trainingData = open("1b_benchmark.dev.tokens")
	for line in trainingData:
		words = line.split()
		words.append("<STOP>")
		N += len(words)
		words.insert(0, "<START>")
		for token in words:
			if token in trainingTokens:
				trainingTokens[token] = trainingTokens[token] + 1
			else:
				trainingTokens[token] = 1

	trainingData.close()
	
	updatedTrainingData = open("1b_benchmark.dev.tokens")
	for line in updatedTrainingData:
		words = line.split()
		words.insert(0, "<START>")
		words.append("<STOP>")
		for i in range(len(words)):
			if i + 1 == len(words):
				break;
			bigram = (words[i], words[i + 1])
			if bigram in bigramTokens:
				bigramTokens[bigram] = bigramTokens[bigram] + 1
			else:
				bigramTokens[bigram] = 1
	updatedTrainingData.close()

	updatedTrainingData = open("1b_benchmark.dev.tokens")
	for line in updatedTrainingData:
		words = line.split()
		words.insert(0, "<START>")
		words.append("<STOP>")
		for i in range(len(words)):
			if i + 2 == len(words):
				break;
			trigram = (words[i], words[i + 1], words[i + 2])
			if trigram in trigramTokens:
				trigramTokens[trigram] = trigramTokens[trigram] + 1
			else:
				trigramTokens[trigram] = 1
	updatedTrainingData.close()

	outFile = open("Dev_Token_Data.txt", "w")
	outFile.write(str(N) + "\n")
	outFile.write(str(trainingTokens))
	biOutFile = open("Dev_Bigram_Data.txt", "w")
	biOutFile.write(str(N) + "\n")
	biOutFile.write(str(bigramTokens))
	triOutFile = open("Dev_Trigram_Data.txt", "w")
	triOutFile.write(str(N) + "\n")
	triOutFile.write(str(trigramTokens))
main()