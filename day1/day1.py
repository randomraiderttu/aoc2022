import os
import fileProcessor as fp

# File variables
fileName = 'inputfile.txt'
fullPathName = os.path.join(os.path.dirname(os.path.realpath(__file__)),fileName)

class Elf:
    def __init__(self, numList) -> None:
        self.calorieList = numList
        self.totalCalories = 0
        self.calculateTotalCalories()

    def calculateTotalCalories(self):
        for num in self.calorieList:
            self.totalCalories += num

def processElves(recs: list[str]) -> list[Elf]:
    tmpList = []
    elfList = []
    for rec in recs:
        if rec:
            tmpList.append(int(rec))
        else:
            tmpElf = Elf(tmpList)
            elfList.append(tmpElf)
            tmpList = []
    return elfList

def findHighestCalorieElf(elves) -> int:
    maxCalories = 0
    for elf in elves:
        maxCalories = max(maxCalories,elf.totalCalories)

    return maxCalories

def findTopThreeTotalCalories(elves) -> int:
    sortedList = sorted(elves, key=lambda x: x.totalCalories, reverse=True)
    return sortedList[0].totalCalories + sortedList[1].totalCalories + sortedList[2].totalCalories


if __name__ == '__main__':
    recs = fp.ingestFile(fullPathName)

    elves = processElves(recs)

    # for num, elf in enumerate(elves):
    #     print(num, elf.totalCalories)

    print(f'Exercise 1: {findHighestCalorieElf(elves)}') 

    print(f'Exercise 2: {findTopThreeTotalCalories(elves)}')  