from os import path
from subprocess import Popen
from urllib.request import urlretrieve


class Fetcher:
    def __init__(self, url="", file=""):
        self.url = url
        self.file = file

    def fetch(self):
        filePath = path.dirname(self.file)
        print(f"Making folder {filePath}/")
        Popen(f"mkdir {filePath}/", shell=True)
        print(f"Downloading {self.file}")
        urlretrieve(self.url, self.file)

    def fetchMissing(self, cleanLine, outPath):
        for line in cleanLine:
            if " as " in line:
                line = line.split(" as ")
                filePath = f"{outPath}/{line[1]}"
                if not path.isfile(filePath):
                    Fetcher(line[0], filePath).fetch()
                cleanLine[cleanLine.index(f"{line[0]} as {line[1]}")] = line[1]
