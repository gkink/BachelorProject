import cv2

def getFrames(filename, startFrame, numFrames):
	cap = cv2.VideoCapture(filename)
	frames = []

	for _ in range(startFrame):
		cap.read()
	for i in range(numFrames):
		ret, frame = cap.read()
		if not ret: 
			break
		frames.append(frame)
	cap.release()

	return frames

def showFrame(filename, frameNum):
	cap = cv2.VideoCapture(filename)
	
	for _ in range(frameNum-1):
		cap.read()
	
	ret, frame = cap.read()
	if not ret: 
		print('error')
		return

	cv2.imshow('frame', frame)
	cv2.waitKey(0)
