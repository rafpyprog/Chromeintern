import os
import platform
from subprocess import check_output, PIPE, Popen, TimeoutExpired
import sys

from . utils import parse_chromedriver_version


n_bits = 64 if sys.maxsize > 2**32 else 32
LINUX_FILENAME = 'chromedriver_linux{}.zip'.format(n_bits)


def get_local_release(executable_path='chromedriver'):
    cmd = [executable_path, '-v']
    try:
        process = Popen(cmd, env=os.environ,
                        close_fds=platform.system() != 'Windows',
                        stdout=PIPE, stderr=PIPE)
    except OSError:
        msg = '{} executable needs to be in PATH.'
        raise WebDriverException(
            msg.format(os.path.basename(executable_path)))
    else:
        stdout = process.communicate()[0]
        version = parse_chromedriver_version(stdout.decode())
    return version
