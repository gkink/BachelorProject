#!/usr/bin/python3

import sys
import cv2
import numpy as np
from removeOutline import getActualBounds
from crop import crop
# startFrame = 200
# numFrames = 150

writeToFolder = False

def pHash(img):
	img = cv2.resize(img, dsize=(8*4,8*4))
	imgDct = cv2.dct(img.astype('float'))[:8,:8]
	avg = (imgDct.sum() - imgDct[0,0]) / (8*8 - 1)
	fp = ''.join(str(int(x <= avg)) for x in imgDct.flatten())
	return fp 

def pHash_sign(img):
	img = cv2.resize(img, dsize=(8*4,8*4))
	imgDct = cv2.dct(img.astype('float'))[:8,:8]
	fp = ''.join(str(int(x <= 0)) for x in imgDct.flatten())
	return fp 

def aHash(img):
	img = cv2.resize(img, dsize=(8,8))
	fp = ''.join(str(x) for x in cv2.threshold(img, img.mean(), 1, cv2.THRESH_BINARY)[1].flatten())
	return fp

hashNameToFn = {'aHash' : aHash, 'pHash' : pHash, 'pHash_sign' : pHash_sign}

def hashFile(videoFile, hashFn='pHash', output=sys.stdout):
	cap = cv2.VideoCapture(videoFile)
	fn = hashNameToFn[hashFn]

	i = 1
	while True:
		ret, frame = cap.read()
		if not ret: break
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		print(fn(frame), file=output)
		if writeToFolder:
			filename = 'frame' + '{0:04}'.format(i) + '.png'
			cv2.imwrite(filename, frame)
			i += 1

def hashFileWithCrop(videoFile, hashFn='pHash', output=sys.stdout):
	cap = cv2.VideoCapture(videoFile)
	fn = hashNameToFn[hashFn]
	frames = []

	while True:
		ret, frame = cap.read()
		if not ret: break
		frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

	cropped = crop(frames)
	for frame in cropped:
		print(fn(frame), file=output)
