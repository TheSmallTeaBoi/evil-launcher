import os
from re import search, split


def readFile(file):
    with open(file, "r") as f:
        f = f.read()
        return f


def sanitize(filter, dirtyList):
    while filter in dirtyList:
        dirtyList.remove(filter)
    return dirtyList


def flatASS(lines):
    newLines = []
    for line in lines:
        newLine = line
        if " as " in line or " with " in line:
            newLine = parseURL(line)
        newLines.append(newLine)
    return newLines


def parseURL(line):
    lineDict = {"wad": ["[", "]"], "config": ["{", "}"], "mod": ["", ""]}
    lineType = "mod"
    if line[0] == "[":
        lineType = "wad"
    if line[0] == "{":
        lineType = "config"

    if " as " in line:
        line = split(" as ", line)[1]
    if " with " in line:
        line = split(" with ", line)[0]
        line += lineDict[lineType][1]

    line = lineDict[lineType][0] + split(" as ", line)[0]
    return line


def clean(filter, string):
    for token in filter:
        string = string.replace(token, "")
    return string


def getMods(filter, dirtyList):
    cleanMods = []

    for item in filter:
        dirtyList = sanitize(item, dirtyList)

    for mod in dirtyList:
        cleanMods.append(mod)

    cleanMods = sanitize("", cleanMods)
    return cleanMods


def getFilepath(file):
    osPath = os.path.dirname(os.path.abspath(file))
    if osPath == ".":
        osPath = ""
    return osPath


def getComments(lines):
    comments = []
    for line in lines:
        if search("^--", line):
            comments.append(line)
    return comments


def listToString(inputList, path):
    finalList = []
    for item in inputList:
        finalList.append('"' + os.path.join(path, os.path.normpath(item)) + '"')
    outputString = " ".join(finalList)
    return outputString
