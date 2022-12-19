import os
import fileProcessor as fp

# File variables
fileName = 'inputfile.txt'
fullPathName = os.path.join(os.path.dirname(os.path.realpath(__file__)),fileName)

class Drop:
    def __init__(self, droplet: list[int]) -> None:
        self.droplet = droplet
        self.adjacentDrops = []

    def checkAdjacentDrop(self, inDrop) -> None:
        # Since I'm running through all the drops to compare, it might be this one I'm comparing - thus exit
        if inDrop.droplet == self.droplet:
            return

        matchCount = 0
        adjacentCheck = 0

        for i in range(3):
            if inDrop.droplet[i] == self.droplet[i]:
                matchCount += 1
            elif abs(inDrop.droplet[i] - self.droplet[i]) == 1:
                adjacentCheck += 1
        
        if matchCount == 2 and adjacentCheck > 0:
            self.adjacentDrops.append(inDrop)

    def sumOpenSides(self) -> int:
        return 6 - len(self.adjacentDrops)

def loadDroplets(drops: list[str]) -> list[Drop]:
    droplets = []
    for drop in drops:
        tmpList = [int(x) for x in drop.split(',')]
        tmpDrop = Drop(tmpList)
        droplets.append(tmpDrop)

    return sorted(droplets, key=lambda x: x.droplet)

def findAdjacentDrops(drops: list[Drop]) -> None:
    for drop in drops:
        for checkDrop in drops:
            drop.checkAdjacentDrop(checkDrop)

def calculateSurfaceArea(drops) -> int:
    total = 0
    for drop in drops:
        total += drop.sumOpenSides()

    return total

def dropExists(dropCoords: list[int], drops: list[Drop]) -> bool:
    for drop in drops:
        if dropCoords == drop.droplet:
            return True
        
    return False

def getMinMax(drops: list[Drop]) -> tuple[int, int, int, int, int, int]:
    minX = 1000
    maxX = 0
    minY = 1000
    maxY = 0
    minZ = 1000
    maxZ = 0

    for drop in drops:
        minX = min(minX, drop.droplet[0])
        maxX = max(maxX, drop.droplet[0])
        minY = min(minY, drop.droplet[1])
        maxY = max(maxY, drop.droplet[1])
        minZ = min(minZ, drop.droplet[2])
        maxZ = max(maxZ, drop.droplet[2])

    return minX, maxX, minY, maxY, minZ, maxZ

def findAirPocketOffset(drops: list[Drop]) -> int:
    airPocketList = []
    # Going through all drop locations between min and max to find any of which are not in the list
    #    and surrounded on all sides by droplets (which indicates this is an air pocket)
    minX, maxX, minY, maxY, minZ, maxZ = getMinMax(drops)

    # Create the empty grid - making it one size bigger all the way around to avoid boundary concerns later
    # Note - had to do my 3d array comprehension in reverse...z then y then x to get the comprehension to work right.
    dropGrid = [[[0 for z in range(minZ-1, maxZ+2)] for y in range(minY-1, maxY+2)] for x in range(minX-1, maxX+2)]

    # Mark the droplets
    for x in range(minX, maxX+1):
        for y in range(minY, maxY+1):
            for z in range(minZ, maxZ+1):
                if dropExists([x,y,z], drops):
                    try:
                        dropGrid[x][y][z] = 1
                    except Exception as e:
                        print(f'Error trying to set the droplet of {x},{y},{z}')
                        raise e

    for x in range(minX, maxX+1):
        for y in range(minY, maxY+1):
            for z in range(minZ, maxZ+1):
                if (dropGrid[x][y][z] == 0 and    # This spot in the grid must be air but surrounded by lava drops
                    dropGrid[x-1][y][z] == 1 and
                    dropGrid[x+1][y][z] == 1 and
                    dropGrid[x][y-1][z] == 1 and
                    dropGrid[x][y+1][z] == 1 and
                    dropGrid[x][y][z-1] == 1 and
                    dropGrid[x][y][z+1] == 1):
                    airPocketList.append([x,y,z])

    for pocket in airPocketList:
        print(pocket)

    return len(airPocketList)                
    

if __name__ == '__main__':
    recs = fp.ingestFile(fullPathName)

    droplets = loadDroplets(recs)

    with open("sortedInputfile.txt", "w") as f:
        for drop in droplets:
            f.write(str(drop.droplet) + '\n')

    findAdjacentDrops(droplets)

    totalCount = calculateSurfaceArea(droplets)

    print(f'Exercise 1 - Surface Area Count: {totalCount}')

    airPocketCount = findAirPocketOffset(droplets)

    print(f'Air Pocket Count: {airPocketCount}')

    print(f'Exercise 2 - Surface Area Count: {totalCount - (6 * airPocketCount)}')

