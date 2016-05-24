#!/usr/bin/python3

import sys
from PIL import Image
import numpy

def generateFingerprint(img):
	img = img.convert('L')
	img = img.resize((8,9), Image.ANTIALIAS)
	arr = numpy.array(img)
	diff = ''
	for row in arr:
		for i in range(1,len(row)):
			if row[i-1] < row[i]: 
				diff += '1'
			else: 
				diff += '0'
	return diff

def main():
	pic = 'lena.png'
	if len(sys.argv) > 1:
		pic = sys.argv[1]
	img = Image.open(pic)
	print(generateFingerprint(img))

if __name__ == '__main__':
	main()