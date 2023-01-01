import os
import fileProcessor as fp
from dataclasses import dataclass
import logging

# File variables
fileName = 'inputfile.txt'
fullPathName = os.path.join(os.path.dirname(os.path.realpath(__file__)),fileName)

@dataclass
class tree():
    treeSize: int
    isVisible: bool
    scenicScore: int = 0
    leftTreeScore: int = 0
    rightTreeScore: int = 0
    upperTreeScore: int = 0
    bottomTreeScore: int = 0

def loadTrees(recs) -> list[list[tree]]:
    tmpMatrix = []
    for rownum, rec in enumerate(recs):
        tmpRow = []
        for t in range(len(rec)):
            # Create a tree class and add it to the row
            if t == 0 or t == len(rec)-1 or rownum == 0 or rownum == len(recs)-1:
                isVisible = True
            else:
                isVisible = False

            tmpTree = tree(int(rec[t]), isVisible)
            tmpRow.append(tmpTree)
        
        # Add the row to the matrix
        tmpMatrix.append(tmpRow)
        
    return tmpMatrix

def findVisibleTrees(treeMatrix):
    for rownum, y in enumerate(treeMatrix):
        for colnum, x in enumerate(y):
            logging.debug('***********************************************')
            logging.debug(f'findVisibleTrees: Testing location [{rownum},{colnum}]')
            if not x.isVisible:
                logging.debug(f'[{rownum},{colnum}], treesize: {x.treeSize} is not marked as visible - checking now')
                leftVisible = True
                rightVisible = True
                topVisible = True
                bottomVisible = True

                for i in range(0,colnum):
                    logging.debug(f'Testing [{rownum},{i}] and treesize is {treeMatrix[rownum][i].treeSize}')
                    if treeMatrix[rownum][i].treeSize >= x.treeSize:
                        logging.debug(f'LeftVisible is False at [{rownum},{i}] due to treesize: {treeMatrix[rownum][i].treeSize}')
                        leftVisible = False
                        break
                for i in range(colnum+1,len(y)):
                    logging.debug(f'Testing [{rownum},{i}] and treesize is {treeMatrix[rownum][i].treeSize}')
                    if treeMatrix[rownum][i].treeSize >= x.treeSize:
                        logging.debug(f'RightVisible is False at [{rownum},{i}] due to treesize: {treeMatrix[rownum][i].treeSize}')
                        rightVisible = False
                        break
                for j in range(0,rownum):
                    logging.debug(f'Testing [{j},{colnum}] and treesize is {treeMatrix[j][colnum].treeSize}')
                    if treeMatrix[j][colnum].treeSize >= x.treeSize:
                        logging.debug(f'RightVisible is False at [{j},{colnum}] due to treesize: {treeMatrix[j][colnum].treeSize}')
                        topVisible = False
                        break
                for j in range(rownum+1,len(treeMatrix)):
                    logging.debug(f'Testing [{j},{colnum}] and treesize is {treeMatrix[j][colnum].treeSize}')
                    if treeMatrix[j][colnum].treeSize >= x.treeSize:
                        logging.debug(f'BottomVisible is False at [{j},{colnum}] due to treesize: {treeMatrix[j][colnum].treeSize}')
                        bottomVisible = False
                        break

                if leftVisible or rightVisible or topVisible or bottomVisible:
                    x.isVisible = True
                else:
                    x.isVisible = False

def countVisibleTrees(treeMatrix) -> int:
    total = 0
    for y in treeMatrix:
        for x in y:
            if x.isVisible:
                total += 1

    return total

def calculateScenicScore(treeMatrix: list[list[tree]]):
    for rownum, y in enumerate(treeMatrix):
        for colnum, x in enumerate(y):
            leftScore = 0
            rightScore = 0
            upperScore = 0
            lowerScore = 0

            # Left score
            for i in range(colnum-1, -1, -1):
                if treeMatrix[rownum][i].treeSize < x.treeSize:
                    leftScore += 1
                else:
                    leftScore += 1
                    break
            # Right score
            for i in range(colnum+1,len(y)):
                if treeMatrix[rownum][i].treeSize < x.treeSize:
                    rightScore += 1
                else:
                    rightScore += 1
                    break
            # Upper score
            for j in range(rownum-1,-1,-1):
                if treeMatrix[j][colnum].treeSize < x.treeSize:
                    upperScore += 1
                else:
                    upperScore += 1
                    break
            # Lower score
            for j in range(rownum+1,len(treeMatrix)):
                if treeMatrix[j][colnum].treeSize < x.treeSize:
                    lowerScore += 1
                else:
                    lowerScore += 1
                    break
            
            x.leftTreeScore = leftScore
            x.rightTreeScore = rightScore
            x.upperTreeScore = upperScore
            x.bottomTreeScore = lowerScore
            x.scenicScore = x.leftTreeScore * x.rightTreeScore * x.upperTreeScore * x.bottomTreeScore

def getHighestScenicScore(treeMatrix) -> int:
    maxScore = 0
    for y in treeMatrix:
        for x in y:
            maxScore = max(x.scenicScore,maxScore)

    return maxScore

def printMatrix(treeMatrix):
    for y in treeMatrix:
        tmpString = ''
        for x in y:            
            tmpString += ' ' + ('*' if x.isVisible else ' ') + str(x.treeSize)
        print(tmpString)

def printMatrixWithScores(treeMatrix):
    for y in treeMatrix:
        tmpString = ''
        for x in y:            
            tmpString += ' ' + str(x.treeSize) + '(' + str(x.scenicScore) + ')'
        print(tmpString)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    recs = fp.ingestFile(fullPathName)

    treeMatrix = loadTrees(recs)

    findVisibleTrees(treeMatrix)

    totalVisibleTrees = countVisibleTrees(treeMatrix)

    print(f'Exercise 1 Total Visible Trees: {totalVisibleTrees}')
    # printMatrix(treeMatrix)

    calculateScenicScore(treeMatrix)

    maxScenicScore = getHighestScenicScore(treeMatrix)

    print(f'Exercise 2 highest scenic score: {maxScenicScore}')

    # printMatrixWithScores(treeMatrix)






    

