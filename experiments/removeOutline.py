# getLevel coupled with searchNonzeros

import numpy as np

levelCache = []

def getActualBounds(frames):
	numFrames = len(frames)
	diffMat = np.zeros(frames[0].shape)
	half = numFrames // 2
	for i in range(half):
		diffMat += (frames[i] - frames[half + i])
	corners = _findOutlineCoordinates(diffMat)
	if None in corners:
		return None
	return _getBounds(corners)

def _findOutlineCoordinates(mat):
	numRows,numCols = mat.shape
	leftUpper  = _searchNonzero(mat, (0,0),                 (1,1))
	rightUpper = _searchNonzero(mat, (0,numCols-1),         (1,-1))
	leftLower  = _searchNonzero(mat, (numRows-1,0),         (-1,1))
	rightLower = _searchNonzero(mat, (numRows-1,numCols-1), (-1,-1))
	return leftUpper, leftLower, rightUpper, rightLower

def _searchNonzero(mat, start, direction):
	numRows,numCols = mat.shape
	i = 0
	while i < numRows and i < numCols:
		level = _getLevel(i)
		for r,c in level:
			currRow = start[0]+r*direction[0]
			currCol = start[1]+c*direction[1]
			if mat[currRow][currCol] != 0 and _checkCorner(mat, (currRow,currCol), direction):
				return (currRow,currCol) 
		i += 1
	return None

def _checkCorner(mat, corner, direction):
	neighbor1 = mat[corner[0] + direction[0]][corner[1]]
	neighbor2 = mat[corner[0]][corner[1] + direction[1]]
	neighbor3 = mat[corner[0] + direction[0]][corner[1] + direction[1]]
	return neighbor1 != 0 or neighbor2 != 0 or neighbor3 != 0

def _getLevel(n):
	if len(levelCache) <= n-1:
		return levelCache[n]
	l = []
	for i in range(n+1):
		l.append( (i,n-i) )
	levelCache.append(l)
	return l

def _getBounds(corners):
	leftUpper, leftLower, rightUpper, rightLower = corners
	leftUpperBound  = max(leftUpper[0],rightUpper[0]), max(leftUpper[1],leftLower[1]) 
	rightLowerBound = min(leftLower[0],rightLower[0]), min(rightUpper[1],rightLower[1])
	return leftUpperBound, rightLowerBound

def main():
	mat = np.zeros((5,6), dtype=np.uint8)
	mat[1:4,1:5] = 1
	mat[1,1] = 0
	mat[0,0] = 1
	mat[3,4] = 0
	print(mat)
	corners = _findOutlineCoordinates(mat)
	print(corners)
	print(_getBounds(corners))

if __name__ == '__main__':
	main()

