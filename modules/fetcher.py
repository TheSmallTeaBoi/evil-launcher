from os import path
from subprocess import call, check_output
from urllib.request import urlretrieve
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
        urlretrieve(self.url, self.file)

    def fetchAndExtract(self, link, outPath):
        # generate 64-character long filename for temp file
        funnyName = "/tmp/" + "".join(choices(ascii_uppercase + digits, k=64))

        Fetcher(link, f"{funnyName}").fetch()

        splitDir = split(r"%%.*%%", outPath)
        outPath = search(r"%%(.*)%%", outPath).group(1)
        print(f"unar -D -o {splitDir[0]}{outPath} {funnyName}")
        check_output(f"unar -D -o {splitDir[0]}{outPath} {funnyName}", shell=True)

    def fetchMissing(self, cleanLine, outPath):
        for line in cleanLine:
            if " as " in line:
                line = line.split(" as ")
                filePath = f"{outPath}/{line[1]}"
                if not path.isfile(hellparser.clean("%", filePath)):
                    if search(r"%%.*%%", filePath):
                        Fetcher().fetchAndExtract(line[0], f"{outPath}/{line[1]}")
                    else:
                        print(f"No match: {line[0]}{line[1]}")
                        Fetcher(line[0], filePath).fetch()
                cleanLine[cleanLine.index(f"{line[0]} as {line[1]}")] = line[1]
        return cleanLine
