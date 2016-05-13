#!/usr/bin/python3

import sys
from PIL import Image
import numpy
from scipy.fftpack import dct

def generateFingerprint(img):
	img = img.convert('L')
	img = img.resize((32,32), Image.ANTIALIAS)
	dctOfImg = dct(img, 2)
	arr = numpy.zeros((8,8))
	for i in range(8):
		for j in range(8):
			arr[i][j] = dctOfImg[i][j]
	average = numpy.average(arr)
	diff = ''
	for row in arr:
		for c in row:
			if c >= average: 
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