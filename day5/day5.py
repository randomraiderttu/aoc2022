import os
import fileProcessor as fp
import queue

# File variables
fileName = 'inputfile.txt'
fullPathName = os.path.join(os.path.dirname(os.path.realpath(__file__)),fileName)

class crateStack:
    def __init__(self, inputList: list[str], crateNum: int) -> None:
        self.stackList = inputList.copy()
        self.stackList2 = inputList.copy()
        self.crateNumber = crateNum

    def pop(self) -> str:
        crate = self.stackList.pop()
        return crate

    def push(self, crate: str) -> None:
        self.stackList.append(crate)

    def grabCrates(self, moveNum) -> list[str]:
        tmpList = self.stackList2[(-1*moveNum):]
        for i in range(moveNum):
            tmpPop = self.stackList2.pop()

        return tmpList

    def addCrates(self, crateList: list[str]):
        self.stackList2.extend(crateList)

class instruction:
    def __init__(self, instructionSet: list[str]) -> None:
        self.instructionSet = instructionSet
        self.processInstructionSet()

    def processInstructionSet(self):
        tmpList = self.instructionSet.split()
        self.numToMove = int(tmpList[1])
        self.fromStack = int(tmpList[3])
        self.toStack = int(tmpList[5])

def splitInputfile(recs: list[str]) -> tuple[list[str], list[str]]:
    crateInput = []
    instructionInput = []
    boolSplitMarker = False

    for rec in recs:
        if not rec:
            boolSplitMarker = True
            continue

        if boolSplitMarker:
            instructionInput.append(rec)
        else:
            crateInput.append(rec)

    # Get the crate input in bottom to top order to make it easier to add to my queues
    crateInput.reverse()

    return crateInput, instructionInput

def getCrateMatrix(crateInput: list[str]) -> list[list]:
    crateList = [int(crateInput[0][i:i+4].strip()) for i in range(0, len(crateInput[0]), 4)]
    tmpCrateMatrix = []
    for i in crateList:
        tmpStack = [i]
        tmpCrateMatrix.append(tmpStack)
    
    for j in crateInput[1:]:
        tmpList = [j[i:i+4] for i in range(0, len(j), 4)]

        for key, item in enumerate(tmpList):
            strippedItem = item.strip().replace(']','').replace('[','')
            if strippedItem:
                tmpCrateMatrix[key].append(strippedItem)

    return tmpCrateMatrix

def loadCrateStacks(crateMatrix: list[list]) -> list[crateStack]:
    tmpList = []

    for stack in crateMatrix:
        tmpCrateStack = crateStack(stack[1:], stack[0])
        tmpList.append(tmpCrateStack)

    return tmpList

def loadInstructions(instructionSet: list[str]) -> list[instruction]:
    tmpList = []

    for rec in instructionSet:
        tmpInstructionSet = instruction(rec)
        tmpList.append(tmpInstructionSet)

    return tmpList

def executeInstructions(crateStacks: list[crateStack], instructionList: list[instruction]):
    for instruction in instructionList:
        # print(f'Move {instruction.numToMove} from {instruction.fromStack} to {instruction.toStack}')
        for move in range(instruction.numToMove):
            poppedCrate = crateStacks[instruction.fromStack-1].pop()
            crateStacks[instruction.toStack-1].push(poppedCrate)
            # print(f'    I moved {poppedCrate} from {crateStacks[instruction.fromStack-1].crateNumber} to {crateStacks[instruction.toStack-1].crateNumber}')

def executeInstructions2(crateStacks: list[crateStack], instructionList: list[instruction]):
    for instruction in instructionList:
        # print(f'Move {instruction.numToMove} from {instruction.fromStack} to {instruction.toStack}')
        cratesToMove = crateStacks[instruction.fromStack-1].grabCrates(instruction.numToMove)
        crateStacks[instruction.toStack-1].addCrates(cratesToMove)
        # print(f'    I moved {cratesToMove} from {crateStacks[instruction.fromStack-1].crateNumber} to {crateStacks[instruction.toStack-1].crateNumber}')


def getTopCrates(crateStacks: list[crateStack]) -> str:
    answer = ''
    for i in crateStacks:
        answer = answer + i.stackList[-1]

    return answer

def getTopCrates2(crateStacks: list[crateStack]) -> str:
    answer = ''
    for i in crateStacks:
        answer = answer + i.stackList2[-1]

    return answer

if __name__ == '__main__':
    recs = fp.ingestFile(fullPathName)

    crateInput, instructionInput = splitInputfile(recs)

    crateMatrix = getCrateMatrix(crateInput)

    crateStacks = loadCrateStacks(crateMatrix)

    instructionList = loadInstructions(instructionInput)

    executeInstructions(crateStacks, instructionList)

    answer1 = getTopCrates(crateStacks)

    print(f'Exercise1 Top Crates are: {answer1}')

    executeInstructions2(crateStacks, instructionList)

    answer2 = getTopCrates2(crateStacks)

    print(f'Exercise2 Top Crates are: {answer2}')
