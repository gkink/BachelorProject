#!/usr/bin/python3

import sys

def main():
	if len(sys.argv) < 4:
		print('./hamming.py [flag] [input0] [input1]')
		return
	flag = sys.argv[1]
	if flag == '-s':
		print(hammingDistance(sys.argv[2], sys.argv[3]))
	if flag == '-r':
		compareFiles(sys.argv[2], sys.argv[3])

def hammingDistance(s1,s2):
	distance = 0
	for i in range(min(len(s1),len(s2))):
		distance += s1[i] != s2[i]
	return distance		

def compareFiles(f1,f2):
	contents1 = [s.strip() for s in open(f1, 'r').readlines()]
	contents2 = [s.strip() for s in open(f2, 'r').readlines()]
	for i in range(len(contents1)):
		for j in range(len(contents2)):
			c1 = contents1[i]
			c2 = contents2[j]
			distance = hammingDistance(c1,c2)
			if distance <= 11:
				print(c1, '-', i)
				print(c2, '-', j)
				print(distance)


if __name__ == '__main__':
	main()