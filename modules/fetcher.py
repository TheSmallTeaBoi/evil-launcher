import hashlib
from os import path

from re import search, split, compile, match, IGNORECASE
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
        if algorithm in self.checksumAlgos:
            algo = self.checksumAlgos[algorithm]()
        else:
            logging.error(f"Invalid algorithm name: {algorithm}. Removing file")
            execute(f"rm {file}")
            exit()
        with open(file, "rb") as f:
            while True:
                data = f.read(65536)
                if not data:
                    break

        if checksum == algo.hexdigest():
            logging.info("Checksums match.")
            return True
        else:
            logging.error("Checksums don't match. Removing file.")
            logging.error(f"Got: {algo.hexdigest()}")
            logging.error(f"Expected: {checksum}")
            execute(f"rm {file}")
            exit()

    def checkURI(self, uri):
        regex = compile(
            r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)",
            IGNORECASE,
        )
        return match(regex, uri) is not None

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
        lineNum = 0
        for line in cleanLine:
            lineNum += 1
            logging.debug(f"fetchMissing: {lineNum}. {line}")

            # Check if line is a comment
            if search("^--", line):
                continue

            # Check if there's a properly formed `with` statement
            if search(" with .+", line):
                checklist = line.split(" with ")[1].split(" ")
                algo = checklist[0]
                checksum = checklist[1]
                line = line.split(" with ")[0]
            elif " with " in line or " with" in line:
                logging.error(f"Syntax error at line {lineNum} (with what?)")
                exit()

            # Check if there's a properly formed `as` statement
            if search(" as .+", line):
                line = line.split(" as ")
                url = line[0]
                if not self.checkURI(url):
                    logging.warn(f"Possibly not a URL: {url}")
                filePath = f"{outPath}/{line[1]}"
                if dryRun:
                    logging.info(
                        f"Found {url}, which would be downloaded to {filePath}"
                    )
                elif not path.isfile(hellparser.clean("%", filePath)):
                    if search(r"%%.*%%", filePath):
                        self.fetchAndExtract(
                            link=url,
                            outPath=filePath,
                            removeTemp=removeTemp,
                            checksum=checksum,
                            algo=algo,
                        )
                    else:
                        logging.info(f"No match: {line[0]}{line[1]}")
                        self.fetch(url=url, file=filePath, checksum=checksum, algo=algo)
            elif " as " in line or " as" in line:
                logging.error(f"Syntax error at line {lineNum} (as what?)")
                exit()
