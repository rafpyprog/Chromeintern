import os
import platform
from subprocess import PIPE, Popen

from selenium.common.exceptions import WebDriverException

from . exceptions import ChromedriverNotFoundException
from . utils import parse_chromedriver_version


n_bits, linkage = platform.architecture()
LINUX_FILENAME = 'chromedriver_linux{}.zip'.format(n_bits[:2])
CMD = 'chromedriver'


def get_local_release(executable_path=''):
    cmd = os.path.join(executable_path, CMD)
    with Popen([cmd, '-v'], close_fds=True, stdout=PIPE,
               universal_newlines=True) as process:
        stdout = process.stdout.read()

    version = parse_chromedriver_version(stdout.strip())
    return version


def linux_get_path():
    cmd = ['which', CMD]
    driver_current_dir = os.path.join(os.getcwd(), CMD)
    driver_in_current_dir = os.path.isfile(driver_current_dir)

    with Popen(cmd, close_fds=True, stdout=PIPE,
               universal_newlines=True) as process:
        path = process.stdout.read()

    NOT_FOUND = 1
    if process.returncode == NOT_FOUND:
        if driver_in_current_dir:
            path = driver_current_dir
        else:
            raise ChromedriverNotFoundException

    return path
