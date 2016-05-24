#!/usr/bin/python3

import sys
import cv2
import numpy as np
import videoUtils
from removeOutline import getActualBounds

startFrame = 0
numFrames = 1000

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

	frames = videoUtils.getFrames(argv[1], startFrame, numFrames)
	frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) for frame in frames]
	upperLeft, lowerRight = getActualBounds(frames)
	frames = [frame[upperLeft[0]:lowerRight[0],upperLeft[1]:lowerRight[1]] for frame in frames]

	for frame in frames:
		print(fingerprint(frame))
		if writeToFolder:
			filename = 'frame' + str(startFrame + i) + '.png'
			cv2.imwrite(filename, gray)


if __name__ == '__main__':
	main(sys.argv)