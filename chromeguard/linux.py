import os
import platform
from subprocess import PIPE, Popen

from . utils import parse_chromedriver_version


n_bits, linkage = platform.architecture()
LINUX_FILENAME = 'chromedriver_linux{}.zip'.format(n_bits[:2])
CMD = 'chromedriver'


def get_local_release(executable_path=''):
    cmd = os.path.join(executable_path, CMD)
    with Popen([cmd, '-v'], close_fds=True, stdout=PIPE,
               universal_newlines=True) as process:
        stdout = process.stdout.read()
        stdout.kill()

    version = parse_chromedriver_version(stdout.strip())
    return version
