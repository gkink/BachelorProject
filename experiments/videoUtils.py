import cv2

def getFrames(filename, startFrame, numFrames):
	cap = cv2.VideoCapture(filename)
	frames = []

	for i in range(startFrame):
		cap.read()
	for i in range(numFrames):
		ret, frame = cap.read()
		if not ret: 
			break
		frames.append(frame)
	cap.release()

	return frames