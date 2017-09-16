import os
from subprocess import check_output, PIPE, Popen
import sys
from threading  import Thread
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

from selenium.common.exceptions import WebDriverException

from . utils import parse_chromedriver_version


WIN_FILENAME = 'chromedriver_win32.zip'
CMD = 'chromedriver.exe'


def in_path():
    proc = Popen('where ' + CMD, env=os.environ, stdout=PIPE, stderr=PIPE,
                 close_fds=False)
    stdout, stderr = proc.communicate()
    status = proc.returncode
    if status == 0:
        return True
    elif status == 1:
        return False
    else:
        raise OSError('Error while searching path.')


def get_local_release(executable_path=None):
    if executable_path:
        cmd = os.path.join(executable_path, CMD)
    else:
        cmd = CMD

    def enqueue_output(out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()

<<<<<<< HEAD
    ON_POSIX = 'posix' in sys.builtin_module_names
    p = Popen([cmd], stdout=PIPE, bufsize=1, close_fds=ON_POSIX)
    q = Queue()
    t = Thread(target=enqueue_output, args=(p.stdout, q))
    t.daemon = True # thread dies with the program
    t.start()
=======
    with proc:
        stdout, stderr = proc.communicate(timeout=5)
        proc.kill()
>>>>>>> fac2eba703c0a9cabeedc56d5b867c9652398a41

    stdout = None
    while not stdout:
        try:
            stdout = q.get_nowait() # or q.get(timeout=.1)
        except Empty:
            pass # no output yet
        else:
            p.kill()

    while not p.poll():
        pass #wait process finish

    version = parse_chromedriver_version(stdout.decode().strip())
    return version


def win_get_path():
    ''' Returns path to Chromedriver or None '''
    assert sys.platform == 'win32'
    cmd = ['where', 'chromedriver']
    stdout = check_output(cmd).decode().strip()
    path = os.path.dirname(stdout)
    return path
