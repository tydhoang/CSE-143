#! /usr/bin/env python3
import fileinput
import sys

def main():
	N = 0
	trainingData = open("1b_benchmark.dev.tokens")
	for line in trainingData:
		words = line.split()
		words.append("<STOP>")
		N += len(words)
		
	outFile = open("Dev_Token_Data.txt", "w")
	outFile.write(str(N))
main()