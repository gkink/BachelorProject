import numpy as np

def removeOutline(frames):
	numFrames = len(frames)
	diffMat = np.zeros(frames[0].shape)
	half = numFrames // 2
	for i in range(half):
		diffMat += (frames[i] - frames[half + i])
	corners = findOutlineCoordinates(diffMat)

def findOutlineCoordinates(mat):
	numRows,numCols = mat.shape
	leftUpper  = searchNonzero(mat, (0,0),                 (1,1))
	rightUpper = searchNonzero(mat, (0,numCols-1),         (1,-1))
	leftLower  = searchNonzero(mat, (numRows-1,0),         (-1,1))
	rightLower = searchNonzero(mat, (numRows-1,numCols-1), (-1,-1))
	return [leftUpper, leftLower, rightUpper, rightLower]

def searchNonzero(mat, start, direction):
	numRows,numCols = mat.shape
	i = 0
	while i < numRows and i < numCols:
		level = getLevel(i)
		for r,c in level:
			currRow = start[0]+r*direction[0]
			currCol = start[1]+c*direction[1]
			if mat[currRow][currCol] != 0 and checkCorner(mat, (currRow,currCol), direction):
				return (currRow,currCol) 
		i += 1
	return None

def checkCorner(mat, corner, direction):
	neighbor1 = mat[corner[0] + direction[0]][corner[1]]
	neighbor2 = mat[corner[0]][corner[1] + direction[1]]
	neighbor3 = mat[corner[0] + direction[0]][corner[1] + direction[1]]
	return neighbor1 != 0 or neighbor2 != 0 or neighbor3 != 0

def getLevel(n):
	l = []
	for i in range(n+1):
		l.append( (i,n-i) )
	return l
	