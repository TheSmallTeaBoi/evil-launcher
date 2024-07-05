import hashlib
from os import path
from subprocess import call, check_call

from re import search, split
import logging
from modules import hellparser
from modules.execute import execute


class Fetcher:
    def __init__(self, url="", file=""):
        self.url = url
        self.file = file
        self.checksumAlgos = {
            "sha256": hashlib.sha256,
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
        }

    def checkSum(self, file, checksum, algorithm):
        algo = self.checksumAlgos[algorithm]()
        with open(file, "rb") as f:
            while True:
                data = f.read(65536)
                if not data:
                    break

        if checksum == algo.hexdigest():
            logging.info("Checksums match.")
            return True
        else:
            logging.error("Checksums don't match. Exiting.")
            logging.error(f"Got: {algo.hexdigest()}")
            logging.error(f"Expected: {checksum}")
            exit()

    def fetch(self, file, url, checksum="", algo=""):
        filePath = path.dirname(file)
        logging.info(f"Making folder {filePath}/")
        execute(f"mkdir -p {filePath}/")
        logging.info(f"Downloading {file}")
        execute(f"wget -c -O '{file}' '{url}'")
        if checksum:
            logging.info("Checking checksum")
            self.checkSum(file, checksum, algo)

    def fetchAndExtract(self, link, outPath, removeTemp=False, checksum="", algo=""):
        # generate change for temp file name
        funnyName = "/tmp/" + hashlib.sha256(link.encode("utf-8")).hexdigest()

        self.fetch(funnyName, link, checksum, algo)

        splitDir = split(r"%%.*%%", outPath)
        outPath = splitDir[0] + search(r"%%(.*)%%", outPath).group(1)
        execute(f"unar -D -o {outPath} {funnyName}")
        if removeTemp:
            logging.warn(f"Deleting temp file `{funnyName}`")
            execute(f"rm {funnyName}")

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
                    logging.info(
                        f"Found {line[0]}, which would be downloaded to {filePath}"
                    )
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
                        logging.info(f"No match: {line[0]}{line[1]}")
                        self.fetch(line[0], filePath, checksum, algo)
