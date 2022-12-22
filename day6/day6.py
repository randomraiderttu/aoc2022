import os
import fileProcessor as fp

# File variables
fileName = 'inputfile.txt'
fullPathName = os.path.join(os.path.dirname(os.path.realpath(__file__)),fileName)

def findSignalMarker(signal: str, distinctLength: int) -> int:
    signalLength = len(signal)
    for i in range(distinctLength,signalLength):
        # print()
        tmpList = list(signal[i-distinctLength:i])
        # print(f'4 character test list is: {sorted(tmpList)}')
        # print(f'Converted list from set is: {sorted(list(set(tmpList)))}')
        if sorted(tmpList) == sorted(list(set(tmpList))):
            return i

    raise Exception('Signal Marker Not Found')        

if __name__ == '__main__':
    recs = fp.ingestFile(fullPathName)

    signalString = recs[0]

    signalMarker = findSignalMarker(signalString, 4)

    print(f'Exercise 1 - Signal Marker is at position {signalMarker}')
    
    messageMarker = findSignalMarker(signalString, 14)

    print(f'Exercise 2 - Mesage Marker is at position {messageMarker}')
