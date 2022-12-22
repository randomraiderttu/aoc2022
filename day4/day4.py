import os
import fileProcessor as fp

# File variables
fileName = 'inputfile.txt'
fullPathName = os.path.join(os.path.dirname(os.path.realpath(__file__)),fileName)

class elfPair:
    def __init__(self, elfPairString: str) -> None:
        self.originalString = elfPairString
        self.setElfSections()

    def getElfSectionSet(self, sectionString: str) -> set:
        tmpList = []
        for i in range(int(sectionString[:sectionString.index('-')]), int(sectionString[sectionString.index('-')+1:])+1):
            tmpList.append(i)

        return set(tmpList)

    def setElfSections(self):
        self.elfSetOne = self.getElfSectionSet(self.originalString.split(',')[0])
        self.elfSetTwo = self.getElfSectionSet(self.originalString.split(',')[1])
        
    def isSetContained(self):
        if ((self.elfSetOne & self.elfSetTwo) == self.elfSetOne or (self.elfSetOne & self.elfSetTwo) == self.elfSetTwo):
            return True
        
        return False

    def containsSetOverlap(self):
        if self.elfSetOne & self.elfSetTwo:
            return True
        
        return False


def loadElfPairs(elfPairList: list[str]) -> list[elfPair]:
    tmpElfList = []

    for pair in elfPairList:
        tmpPair = elfPair(pair)
        tmpElfList.append(tmpPair)

    return tmpElfList

def countContainedElfPairs(elfPairs: list[elfPair]) -> int:
    total = 0
    
    for pair in elfPairs:
        if pair.isSetContained():
            total += 1

    return total

def countOverlappingElfPairs(elfPairs: list[elfPair]) -> int:
    total = 0
    
    for pair in elfPairs:
        if pair.containsSetOverlap():
            total += 1

    return total

if __name__ == '__main__':
    recs = fp.ingestFile(fullPathName)

    elfPairs = loadElfPairs(recs)

    totalContainedPairs = countContainedElfPairs(elfPairs)

    print(f'Exercise 1 Total Elf Pairs Contained: {totalContainedPairs}')

    totalOverlappingPairs = countOverlappingElfPairs(elfPairs)

    print(f'Exercise 2 Total Elf Pairs Overlapping: {totalOverlappingPairs}')
