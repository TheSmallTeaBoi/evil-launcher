import logging
import subprocess
import shlex


def execute(system_command, **kwargs):
    """Execute a system command, passing STDOUT and STDERR to logger.

    Source: https://stackoverflow.com/a/4417735/2063031
    """
    logging.info("Running: '%s'", system_command)
    popen = subprocess.Popen(
        shlex.split(system_command),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        **kwargs,
    )
    for stdout_line in iter(popen.stdout.readline, ""):
        logging.debug(stdout_line.strip())
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        logging.warn(f"`{system_command}` exited with code {return_code}")
        raise subprocess.CalledProcessError(return_code, system_command)
