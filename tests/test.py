import os
import platform
import pytest
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from chromintern import Chromintern
from chromintern.linux import LINUX_FILENAME
from chromintern.mac import MAC_FILENAME
from chromintern.win import WIN_FILENAME, get_local_release, in_path


TESTS_FOLDER = os.path.join(os.getcwd(), 'tests')
PLATFORM = platform.system()
TEST_RELEASE = '2.20'

if PLATFORM == 'Windows':
    def test_win_get_local_release():
        tmp = TemporaryDirectory()
        os.chdir(tmp.name)
        with ZipFile(os.path.join(TESTS_FOLDER, WIN_FILENAME)) as z:
            z.extractall(tmp.name)
        release = get_local_release(tmp.name)
        assert in_path()
        assert release == TEST_RELEASE


    def test_win_in_path():
        assert in_path() is False
