#!/usr/bin/python3

import sys
from collections import Counter

def main():
	if len(sys.argv) < 4:
		print('Usage: ./hamming.py [flag] [small_file] [large_file]')
		return
	flag = sys.argv[1]
	if flag == '-s':
		print(hammingDistance(sys.argv[2], sys.argv[3]))
	if flag == '-r':
		compareFiles(sys.argv[2], sys.argv[3])

def hammingDistance(s1,s2):
	distance = 0
	for i in range(min(len(s1),len(s2))):
		distance += int(s1[i] != s2[i])
	return distance		

def compareFiles(f1,f2,output=sys.stdout,threshold=10):			
	needles = list(Counter([s.strip() for s in open(f1, 'r').readlines()]).items())
	with open(f2, 'r') as haystack:
		i = 0
		for current_hash in haystack:
			current_hash = current_hash.strip()
			for j in range(len(needles)):
				(current_needle,weight) = needles[j]
				distance = hammingDistance(current_needle, current_hash)
				if distance <= threshold:
					print(current_needle, '-', j, file=output)
					print(current_hash, '-', i, file=output)
					print('distance', distance, file=output)
					print('weight', weight, file=output)
			i += 1

if __name__ == '__main__':
	main()

