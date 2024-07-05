import hashlib
from os import path
from subprocess import call, check_call
import hashlib

from re import search, split
from modules import hellparser


class Fetcher:
    def __init__(self, url="", file=""):
        self.url = url
        self.file = file
        self.checksumAlgos = {"sha256": hashlib.sha256, "md5": hashlib.md5}

    def checkSum(self, file, checksum, algorithm):
        algo = self.checksumAlgos[algorithm]()
        with open(file, "rb") as f:
            while True:
                data = f.read(65536)
                if not data:
                    break

        print(f"Got: {algo.hexdigest()}")
        print(f"Expected: {checksum}")
        if checksum == algo.hexdigest():
            print("Checksums match.")
            return True
        else:
            print("Checksums don't match.")
            return False

    def fetch(self, file, url, checksum="", algo=""):
        filePath = path.dirname(file)
        print(f"Making folder {filePath}/")
        call(f"mkdir -p {filePath}/", shell=True)
        print(f"Downloading {file}")
        check_call(f"wget -c -O '{file}' '{url}'", shell=True)
        if checksum:
            print("Checking checksum")
            self.checkSum(file, checksum, algo)

    def fetchAndExtract(self, link, outPath, removeTemp=False, checksum="", algo=""):
        # generate change for temp file name
        funnyName = "/tmp/" + hashlib.sha256(link.encode("utf-8")).hexdigest()

        self.fetch(funnyName, link, checksum, algo)

        splitDir = split(r"%%.*%%", outPath)
        outPath = splitDir[0] + search(r"%%(.*)%%", outPath).group(1)
        check_call(f"unar -D -o {outPath} {funnyName}", shell=True)
        if removeTemp:
            print(f"Deleting temp file `{funnyName}`")
            call(f"rm {funnyName}", shell=True)

    def fetchMissing(self, cleanLine, outPath, removeTemp=False, dryRun=False):
        checksum, algo = "", ""
        for line in cleanLine:
            if " with " in line:
                checklist = line.split(" with ")[1].split(" ")
                algo = checklist[0]
                checksum = checklist[1]
                line = line.split(" with ")[0]

            if " as " in line:
                line = line.split(" as ")
                filePath = f"{outPath}/{line[1]}"
                if dryRun:
                    print(f"Found {line[0]}, which would be downloaded to {filePath}")
                elif not path.isfile(hellparser.clean("%", filePath)):
                    if search(r"%%.*%%", filePath):
                        self.fetchAndExtract(
                            line[0],
                            f"{outPath}/{line[1]}",
                            removeTemp=removeTemp,
                            checksum=checksum,
                            algo=algo,
                        )
                    else:
                        print(f"No match: {line[0]}{line[1]}")
                        self.fetch(line[0], filePath, checksum, algo)
