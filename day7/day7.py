import os
import fileProcessor as fp
from dataclasses import dataclass

# File variables
fileName = 'inputfile.txt'
fullPathName = os.path.join(os.path.dirname(os.path.realpath(__file__)),fileName)

@dataclass
class file():
    name: str
    size: int

class directory():
    def __init__(self, dirName: str, parentDir) -> None:
        self.directoryName = dirName
        self.parentDirectory = parentDir
        self.directorySize = 0
        self.fileList = []       # List of file classes
        self.directoryList = []  # List of directory name strings

    def updateDirectorySize(self):
        self.directorySize = 0
        for file in self.fileList:
            self.directorySize += file.size
        for dir in self.directoryList:
            self.directorySize += dir.directorySize     

    def fileExists(self, fileName: str) -> bool:
        for file in self.fileList:
            if fileName == file.name:
                return True
        return False

    def directoryExists(self, inDir) -> bool:
        for dir in self.directoryList:
            if dir.directoryName == inDir.directoryName:
                return True
        return False

    def addFile(self, fileString: str):
        tmpFileParts = fileString.split()
        if not self.fileExists(tmpFileParts[1]):
            tmpFile = file(name=tmpFileParts[1], size=int(tmpFileParts[0]))
            self.fileList.append(tmpFile)
            self.updateDirectorySize()

    def addDirectory(self, dir):
        if not self.directoryExists(dir):
            self.directoryList.append(dir)
 
    def getDirectorySize(self) -> int:
        return self.directorySize

def changeDirectory(currentDirectory: directory, directoryName: str) -> directory:
    for dir in currentDirectory.directoryList:
        if dir.directoryName == directoryName:
            return dir
        else:
            continue
    raise Exception(f'Unable to locate directory')

def processCommand(command: str, currentDirectory: directory, dirList: list[directory]) -> directory:
    try:
        commandList = command.split()
        # print(f'Command: {command} and Current Directory: {currentDirectory.directoryName}')

        if commandList[0] == '$':
            if commandList[1] == 'cd':
                if commandList[2] == '..':
                    # print(f'Move up a directory')
                    return currentDirectory.parentDirectory
                elif commandList[2] != '/':
                    # print(f'Move to {commandList[2]}')
                    return changeDirectory(currentDirectory, commandList[2])
                else:
                    # If we're here, it's cd / which is root and we know that's at the first position in dirList
                    return dirList[0]

            elif commandList[1] == 'ls':
                    return currentDirectory
            else:
                raise Exception(f'Unknown command at prompt: {command}')
        elif commandList[0] == 'dir':
            tmpDirectory = directory(dirName=commandList[1], parentDir=currentDirectory)
            # print(f'Added {tmpDirectory.directoryName}')
            currentDirectory.addDirectory(dir=tmpDirectory)
            dirList.append(tmpDirectory)
            # print('****Printing all Directories in List')
            # for dir in dirList:
            #     print(f'Directory: {dir.directoryName}')
            # print('*********************')
        elif commandList[0].isdigit():
            # print(f'Adding file: {command}')
            currentDirectory.addFile(command)
        else:
            raise Exception(f'Unknown Command in processCommand function: {command}')
    except Exception as e:
        print(f'Failed on command: {command}')
        printDirectoryTree(dirList[0],0)
        raise e

    return currentDirectory

def calculateDirectorySizes(dir: directory):
    # print(f'On directory {dir.directoryName}')
    for subDir in dir.directoryList:
        # print(f'Working on Sub Directory {subDir.directoryName}')
        calculateDirectorySizes(subDir)

    dir.updateDirectorySize()
    # print(f'Total Size of Directory {dir.directoryName} is {dir.directorySize}')

def getTotalDirectorySizeUnder100k(dirList: list[directory]) -> int:
    total = 0
    for dir in dirList:
        if dir.directorySize <= 100000:
            total += dir.directorySize

    return total

def printDirectoryTree(dir: directory, level: int):
    padString = '--' * level
    print(f'{padString} {dir.directoryName}')

    for subDir in dir.directoryList:
        printDirectoryTree(subDir, level+1)

def getMinDirectoryToDelete(dirList: list[directory]) -> int:
    usedSpace = dirList[0].directorySize
    freeSpace = 70000000 - usedSpace
    spaceNeeded = 30000000 - freeSpace
    print(f'Used space is {usedSpace} and current free space is {freeSpace}, thus i need {spaceNeeded} for the update')
    
    sizeOfDirToDelete = usedSpace
    for dir in dirList:
        if dir.directorySize >= spaceNeeded and dir.directorySize < sizeOfDirToDelete:
            sizeOfDirToDelete = dir.directorySize
    return sizeOfDirToDelete


if __name__ == '__main__':
    recs = fp.ingestFile(fullPathName)

    dirList = []

    tmpDir = directory('/',None)
    dirList.append(tmpDir)

    curDir = tmpDir

    for rec in recs:
        curDir = processCommand(rec, curDir, dirList)
        # input('Press any key to continue')

    calculateDirectorySizes(dirList[0])

    exercise1Total = getTotalDirectorySizeUnder100k(dirList=dirList)

    print(f'Exercise 1 Answer: {exercise1Total}')

    # printDirectoryTree(dirList[0], 0)

    exercise2Size = getMinDirectoryToDelete(dirList=dirList)

    print(f'Exercise 2 Size to Delete: {exercise2Size}')









    

