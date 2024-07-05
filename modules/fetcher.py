import hashlib
from os import path
from subprocess import call, check_call
from hashlib import sha256

from re import search, split
from string import ascii_uppercase, digits
from random import choices
from modules import hellparser


class Fetcher:
    def __init__(self, url="", file=""):
        self.url = url
        self.file = file

    def fetch(self):
        filePath = path.dirname(self.file)
        print(f"Making folder {filePath}/")
        call(f"mkdir -p {filePath}/", shell=True)
        print(f"Downloading {self.file}")
        check_call(f"wget -c -O '{self.file}' '{self.url}'", shell=True)

    def fetchAndExtract(self, link, outPath, removeTemp=False):
        # generate change for temp file name
        funnyName = "/tmp/" + sha256(link.encode("utf-8")).hexdigest()

        Fetcher(link, funnyName).fetch()

        splitDir = split(r"%%.*%%", outPath)
        outPath = splitDir[0] + search(r"%%(.*)%%", outPath).group(1)
        check_call(f"unar -D -o {outPath} {funnyName}", shell=True)
        if removeTemp:
            print(f"Deleting temp file `{funnyName}`")
            call(f"rm {funnyName}", shell=True)

    def fetchMissing(self, cleanLine, outPath, removeTemp=False, dryRun=False):
        cleanLine = hellparser.sanitize("", cleanLine)
        for line in cleanLine:
            if " as " in line:
                line = line.split(" as ")
                filePath = f"{outPath}/{line[1]}"
                if dryRun:
                    print(f"Found {line[0]}, which would be downloaded to {filePath}")
                elif not path.isfile(hellparser.clean("%", filePath)):
                    if search(r"%%.*%%", filePath):
                        Fetcher().fetchAndExtract(
                            line[0], f"{outPath}/{line[1]}", removeTemp
                        )
                    else:
                        print(f"No match: {line[0]}{line[1]}")
                        Fetcher(line[0], filePath).fetch()
                cleanLine[cleanLine.index(f"{line[0]} as {line[1]}")] = line[1]
            else:
                if dryRun:
                    print(f"Found {line}")
        return cleanLine
