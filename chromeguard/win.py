import os
from subprocess import PIPE, Popen

from . utils import parse_chromedriver_version


WIN_FILENAME = 'chromedriver_win32.zip'
CMD = 'chromedriver.exe'


def get_local_release(executable_path=""):
    cmd = os.path.join(executable_path, CMD)

    with Popen([cmd, '-v'], close_fds=False, stdout=PIPE,
               universal_newlines=True) as process:
        stdout = process.stdout.read()

    version = parse_chromedriver_version(stdout.strip())
    return version


def win_get_path():
    ''' Returns path to Chromedriver or None '''
    cmd = ['where', 'chromedriver']
    with Popen(cmd, stdout=PIPE, universal_newlines=True) as p:
        stdout = p.stdout.read()
    '''
    try:
        stdout, errs = p.communicate(timeout=2)
    except TimeoutExpired:
        p.kill()
        stdout, errs = p.communicate()'''

    path = os.path.dirname(stdout.strip())
    return path
