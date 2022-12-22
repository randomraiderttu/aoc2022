import os

def ingestFile(fileName: str) -> list[str]:
    """Takes a file path and name parameter, ingests a file and returns a list from the file.
    Args:
        fileName (string): filename with path
    """
    with open(fileName) as fileObject:
        lines = fileObject.readlines()

    stripLines = [x.rstrip('\n') for x in lines]

    return stripLines

