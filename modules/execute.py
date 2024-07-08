import logging
import subprocess
import shlex
import os


def execute(system_command, **kwargs):
    """Execute a system command, passing STDOUT and STDERR to logger.

    Source: https://stackoverflow.com/a/4417735/2063031
    """

    logging.debug(f"System name is {os.name}")

    command = shlex.split(system_command)

    isWindows = os.name == "nt"

    if isWindows:
        command = [command[0] + ".exe"] + command[1:]

    logging.info(f"Running command\n{command}")
    popen = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        **kwargs,
    )

    # if False:
    for stdout_line in iter(popen.stdout.readline, ""):
        logging.debug(stdout_line.strip())
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        logging.error(f"`{system_command}` exited with code {return_code}")
        exit()
