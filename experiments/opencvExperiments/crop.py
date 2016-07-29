#!/usr/bin/python3

import cv2
import numpy as np
import sys

blur_radius = 15

# argument passed: list of grayscale frames
def crop(frames):
	assert len(frames) > 1, "too few frames"
	
	cropped = []
	for i in range(len(frames)-1):
		diff = frames[i+1] - frames[i]
		affineMatrix, height, width = _getTransformParameters(diff)
		cropped.append(cv2.warpAffine(frames[i],affineMatrix,(width,height)))
	return cropped

def _getTransformParameters(diff):
	blur = cv2.blur(diff, (blur_radius, blur_radius))
	(_,thresh) = cv2.threshold(blur,1,255,cv2.THRESH_BINARY)
	_, contours, _ = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

	height,width = diff.shape
	center = (height//2, width//2)
	area_thresh = height * width // 4
	countour = None
	for cnt in contours:
		if cv2.pointPolygonTest(cnt,center,False) and cv2.contourArea(cnt) > area_thresh:
			contour = cnt
			break

	rect = cv2.minAreaRect(contour)
	box = cv2.boxPoints(rect)
	box = np.int0(box)
	# sort coordinates
	box = box[box[:,0].argsort()]
	if box[0][1] < box[1][1]:
		box[0][1], box[1][1] = box[1][1], box[0][1]
	if box[2][1] > box[3][1]:
		box[2][1], box[3][1] = box[3][1], box[2][1]

	offset = blur_radius//2

	box[0][0] += offset
	box[0][1] -= offset
	box[1][0] += offset
	box[1][1] += offset
	box[2][0] -= offset
	box[2][1] += offset
	box[3][0] -= offset
	box[3][1] -= offset

	height = int(np.linalg.norm(np.array(box[0]) - np.array(box[1])))
	width = int(np.linalg.norm(np.array(box[1]) - np.array(box[2])))

	pts1 = np.float32(box[1:])
	pts2 = np.float32([[0,0],[width-1,0],[width-1,height-1]])
	affineMatrix = cv2.getAffineTransform(pts1,pts2)
	
	return affineMatrix, height, width


def test1():
	from videoUtils import getFrames
	frames = getFrames(sys.argv[1], 0, 200)
	frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) for frame in frames]
	cropped = crop(frames)
	for i in range(len(cropped)):
		cv2.imwrite('diff/crop/frame{0:03}.png'.format(i), cropped[i])

if __name__ == '__main__':
	test1()