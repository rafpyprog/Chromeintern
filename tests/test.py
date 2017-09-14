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


@pytest.mark.windows
@pytest.fixture
def tmp_folder():
    tmp = TemporaryDirectory()
    with ZipFile(os.path.join(TESTS_FOLDER, WIN_FILENAME)) as z:
        z.extractall(tmp.name)
    yield tmp
    # leave the temp folder
    tmp.cleanup()

@pytest.mark.windows
def test_win_get_local_release(tmp_folder):
    with tmp_folder:
        chrome_path = tmp_folder.name
        release = get_local_release(chrome_path)
        assert release == TEST_RELEASE
