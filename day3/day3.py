import os
import fileProcessor as fp
from string import ascii_lowercase, ascii_uppercase

# File variables
fileName = 'inputfile.txt'
fullPathName = os.path.join(os.path.dirname(os.path.realpath(__file__)),fileName)

# Merge dictionaries together to get a map of letter to value
valueMap = {v:k+1 for k, v in enumerate(ascii_lowercase)} | {v:k+27 for k, v in enumerate(ascii_uppercase)}

class ruckSack:
    def __init__(self, ruckSackContents: str) -> None:
        self.ruckSackContents = ruckSackContents
        self.ruckSackTotalItems = len(ruckSackContents)
        self.ruckSackMidpoint = int(self.ruckSackTotalItems/2)
        self.compartmentOne = ruckSackContents[:self.ruckSackMidpoint]
        self.compartmentTwo = ruckSackContents[self.ruckSackMidpoint:]
        self.commonLetters = list(set(self.compartmentOne) & set(self.compartmentTwo))


def loadRuckSacks(ruckSacks: list[str]) -> list[ruckSack]:
    tmpRuckSackList = []
    for ruck in ruckSacks:
        tmpRuck = ruckSack(ruck)
        tmpRuckSackList.append(tmpRuck)

    return tmpRuckSackList

def calculatePrioiritySum(ruckSacks: list[ruckSack], cipher: dict) -> int:
    total = 0

    for ruck in ruckSacks:
        for item in ruck.commonLetters:
            total += cipher[item]

    return total

def getBadgePrioritySum(ruckSacks: list[ruckSack], cipher: dict) -> int:
    total = 0

    for i in range(0,len(ruckSacks),3):
        commonLetter = list(set(ruckSacks[i].ruckSackContents) & set(ruckSacks[i+1].ruckSackContents) & set(ruckSacks[i+2].ruckSackContents))
        total += cipher[commonLetter[0]]

    return total

if __name__ == '__main__':
    recs = fp.ingestFile(fullPathName)

    ruckSacks = loadRuckSacks(recs)

    # for ruck in ruckSacks:
    #     print(f'RuckSack Contents: {ruck.ruckSackContents}, Midpoint: {ruck.ruckSackMidpoint}, Total Items: {ruck.ruckSackTotalItems}, C1: {ruck.compartmentOne}, C2: {ruck.compartmentTwo}, Common Letters: {ruck.commonLetters}')

    totalPriority = calculatePrioiritySum(ruckSacks, valueMap)

    print(f'Exercise 1 Total Priority Summation: {totalPriority}')

    print(f'Exercise 2 Total Badge Priority Summation: {getBadgePrioritySum(ruckSacks, valueMap)}')