from os import path
from re import findall, search, split


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
    lineDict = {"wad": "[", "config": "{", "mod": ""}
    lineType = "mod"
    if line[0] == "[":
        lineType = "wad"
    if line[0] == "{":
        lineType = "config"

    if " as " in line:
        line = split(" as ", line)[1]
    if " with " in line:
        line = split(" with ", line)[0]
        if lineType == "wad":
            line += "]"
        if lineType == "config":
            line += "}"

    line = lineDict[lineType] + split(" as ", line)[0]
    return line


def clean(filter, string):
    for token in filter:
        string = string.replace(token, "")
    string = string.replace("./", "")
    return string


def getMods(filter, dirtyList, filePath):
    cleanMods = []
    mods = []

    for mod in dirtyList:
        mod = mod.replace("./", "")
        cleanMods.append(mod)

    mods = cleanMods
    mods = sanitize("", mods)
    mods = listToString(mods, filePath)
    return mods


def getFilepath(file):
    osPath = path.dirname(path.abspath(file))
    if osPath == "" or osPath == ".":
        osPath = "./"
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
        finalList.append('"' + path + "/" + item + '"')
    outputString = " ".join(finalList)
    return outputString
