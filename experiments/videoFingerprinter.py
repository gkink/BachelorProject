#!/usr/bin/python3

import sys
import cv2
import numpy as np
import videoUtils

startFrame = 100
numFrames = 100

writeToFolder = False

def fingerprint(img):
	img = cv2.resize(img, dsize=(9,8))
	fp = ''
	for row in range(8):
		for col in range(8):
			fp = fp + str(int(img[row][col] > img[row][col+1]))
	return fp

def main(argv):
	if len(argv) < 2:
		print('specify a videofile')
		return

	for frame in videoUtils.getFrames(argv[1], startFrame, numFrames):
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		print(fingerprint(gray))
		if writeToFolder:
			filename = 'frame' + str(startFrame + i) + '.png'
			cv2.imwrite(filename, gray)


if __name__ == '__main__':
	main(sys.argv)