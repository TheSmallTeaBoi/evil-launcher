from sys import argv
from re import split, findall
from os import path


def readFile(file):
    with open(file, "r") as f:
        f = f.read()
        return f


def sanitize(filter, dirtyList):
    while filter in dirtyList:
        dirtyList.remove(filter)
    return dirtyList


def clean(filter, string):
    for token in filter:
        string = string.replace(token, "")
    return string


def getFilepath(file):
    osPath = path.dirname(file)
    if osPath == "" or osPath == ".":
        osPath = "./"
    return osPath


def getComments(lines):
    comments = []
    for line in lines:
        comments.append(findall(r"\A--.*", line))
    return comments


def listToString(inputList, path):
    finalList = []
    for item in inputList:
        finalList.append('"' + path + item + '"')
    outputString = " ".join(finalList)
    return outputString


def main():
    file = readFile(argv[1])
    filePath = getFilepath(argv[1])
    lines = split("\n", file)

    wad = findall(r"\[.*\]", file)[0]
    config = findall(r"\{.*\}", file)[0]
    comments = getComments(lines)

    # Clean the strings
    mods = sanitize(wad, lines)
    mods = sanitize(config, mods)
    for comment in comments:
        if comment:
            mods = sanitize(comment[0], mods)

    mods = listToString(sanitize("", mods), filePath)
    wad = clean("[]", wad)
    config = clean("{}", config)

    print(f"The hell file is at {filePath}")
    print(f"The wad is {wad}")
    print(f"The config file is {config}")
    print(f"The mods are {mods}")

    print(
        f"""The command would be run as
        `gzdoom -iwad "{filePath}{wad}" -config "{filePath}{config}" -file {mods}
        """
    )
