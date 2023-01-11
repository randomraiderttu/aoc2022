import os
import fileProcessor as fp
from dataclasses import dataclass
import logging
from typing import List

# File variables
fileName = 'inputfile.txt'
fullPathName = os.path.join(os.path.dirname(os.path.realpath(__file__)),fileName)

class Point():
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.locationHistory = ['(0,0)']
    
    def moveUp(self):
        self.y += 1

    def moveDown(self):
        self.y -= 1

    def moveRight(self):
        self.x += 1

    def moveLeft(self):
        self.x -= 1

    def getCoordinate(self) -> str:
        return f'({str(self.x)},{str(self.y)})'

    def addCurrentLocationToHistory(self):
        if not self.getCoordinate() in self.locationHistory:
            self.locationHistory.append(self.getCoordinate())

@dataclass
class Instruction():
    direction: str
    moveNum: int

def loadInstructions(recs: list[str]) -> list[Instruction]:
    tmpList = []
    for rec in recs:
        tmpInstruction = Instruction(rec.split()[0], int(rec.split()[1]))
        tmpList.append(tmpInstruction)

    return tmpList

def moveTail(head: Point, tail: Point):
    currentTailCoords = tail.getCoordinate()
    xDiff = head.x - tail.x
    yDiff = head.y - tail.y
    absXDiff = abs(xDiff)
    absYDiff = abs(yDiff)

    if absYDiff == 0 and absXDiff > 1:
        # if head x - tail x is positive, head is to the right of tail - move tail right, else move it left
        if xDiff > 0:
            tail.moveRight()
        else:
            tail.moveLeft()
    elif absXDiff == 0 and absYDiff > 1:
        # if head y - tail y is positive, head is above tail - move tail up, else move tail down
        if yDiff > 0:
            tail.moveUp()
        else:
            tail.moveDown()
    elif absXDiff == 1 and absYDiff > 1:
        # We need to move diagonally - head is right or left of tail and more than one higher or lower
        if xDiff > 0:
            tail.moveRight()
        else:
            tail.moveLeft()

        if yDiff > 0:
            tail.moveUp()
        else:
            tail.moveDown()
    elif absYDiff == 1 and absXDiff > 1:
        # We need to move diagonally - head is up or down of tail and more than one right or left
        if yDiff > 0:
            tail.moveUp()
        else:
            tail.moveDown()

        if xDiff > 0:
            tail.moveRight()
        else:
            tail.moveLeft()

    # Return the new tail - which may be the same if we didn't have to move
    logging.debug(f'Head is at {head.getCoordinate()}. Tail was at {currentTailCoords} and now at {tail.getCoordinate()}')
    # Add the tail's current location to it's location history
    tail.addCurrentLocationToHistory()
    

def moveHead(instruction: Instruction, knotList: list[Point]):
    for step in range(instruction.moveNum):
        match instruction.direction:
            case 'U':
                logging.debug('Moving head up')
                knotList[0].moveUp()
                knotList[0].addCurrentLocationToHistory()
            case 'D':
                logging.debug('Moving head down')
                knotList[0].moveDown()
                knotList[0].addCurrentLocationToHistory()
            case 'R':
                logging.debug('Moving head right')
                knotList[0].moveRight()
                knotList[0].addCurrentLocationToHistory()
            case 'L':
                logging.debug('Moving head left')
                knotList[0].moveLeft()
                knotList[0].addCurrentLocationToHistory()

        # Move all the knots behind Head in order
        for i in range(len(knotList)-1):
            tailCoordinate = moveTail(head=knotList[i], tail=knotList[i+1])

def processInstructions(instructions: list[Instruction], knotList: list[Point]):
    for instruction in instructions:
        logging.debug(f'Current Instruction is to move {instruction.direction} for {instruction.moveNum}')
        moveHead(instruction, knotList)

def setKnotList(knotNum: int) -> list[Point]:
    tmpList = []
    for i in range(knotNum):
        tmpPoint = Point()
        tmpList.append(tmpPoint)
    
    return tmpList

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    recs = fp.ingestFile(fullPathName)

    instructionList = loadInstructions(recs)

    #Process this with two knots for Exercise1
    knotList = setKnotList(2)

    processInstructions(instructionList, knotList)

    tailListSet = set(knotList[-1].locationHistory)

    print(f'Exercise 1 - total coordinates where Tail was is: {len(tailListSet)}')

    #Process this with ten knots for Exercise2
    knotList2 = setKnotList(10)

    processInstructions(instructionList, knotList2)

    tailListSet2 = set(knotList2[-1].locationHistory)

    print(f'Exercise 2 - total coordinates where Tail was is: {len(tailListSet2)}')




    

