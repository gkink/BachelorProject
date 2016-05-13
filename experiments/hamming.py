#!/usr/bin/python3

import sys

def main():
	if len(sys.argv) < 3:
		return
	print(hammingDistance(sys.argv[1], sys.argv[2]))

def hammingDistance(s1,s2):
	distance = 0
	for i in range(min(len(s1),len(s2))):
		distance += s1[i] != s2[i]
	return distance		

if __name__ == '__main__':
	main()