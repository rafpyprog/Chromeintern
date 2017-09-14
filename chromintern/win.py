import os
import platform
from subprocess import check_output, PIPE, Popen
from subprocess import TimeoutExpired

from selenium.common.exceptions import WebDriverException

from . utils import parse_chromedriver_version


WIN_FILENAME = 'chromedriver_win32.zip'
CMD = 'chromedriver'


def in_path():
    proc = Popen(['where', CMD], stdout=PIPE, stderr=PIPE)
    stdout, stderr = proc.communicate()
    status = proc.returncode
    if status == 0:
        return stdout.decode().splitlines()
    elif status == 1:
        return False
    else:
        raise OSError('Error while searching path.')

in_path()


def get_local_release(executable_path=None):
    cmd = os.path.join(executable_path, CMD)

    try:
        proc = Popen(cmd, env=os.environ, stdout=PIPE, stderr=PIPE,
                     close_fds=platform.system() != 'Windows')
    except OSError:
        msg = '{} executable needs to be in PATH.'
        raise WebDriverException(
            msg.format(executable_path))
    else:
        try:
            outs, errs = proc.communicate(timeout=0.5)
        except TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
    version = parse_chromedriver_version(stdout.decode())
    return version
