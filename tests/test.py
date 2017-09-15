import os
import platform
import pytest
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from chromintern import Chromintern
from chromintern.linux import LINUX_FILENAME
from chromintern.mac import MAC_FILENAME
from chromintern.win import WIN_FILENAME, get_local_release, in_path
from chromintern.utils import powershell_get_latest_release


TESTS_FOLDER = os.path.join(os.getcwd(), 'tests')
PLATFORM = platform.system()
TEST_RELEASE = '2.20'


@pytest.fixture
def tmp_folder():
    tmp = TemporaryDirectory()
    #tmp = os.path.expanduser('~')
    with ZipFile(os.path.join(TESTS_FOLDER, WIN_FILENAME)) as z:
        #z.extractall(tmp)
        z.extractall(tmp.name)
    yield tmp
    # leave the temp folder
    tmp.cleanup()
    #os.remove(os.path.join(tmp, WIN_FILENAME))


###########################################################################
# WINDOWS
############################################################################


@pytest.mark.windows
def test_win_get_local_release(tmp_folder):
    with tmp_folder:
        chrome_path = tmp_folder.name
        release = get_local_release(chrome_path)
    assert release == TEST_RELEASE


@pytest.mark.windows
def test_win_in_path_true(tmp_folder):
    with tmp_folder:
        assert in_path() is True


###########################################################################
# CHROMINTERN
############################################################################

@pytest.mark.chromeintern
def test_chromintern_get_local_release(tmp_folder):
    with tmp_folder:
        c = Chromintern()
        c.path = tmp_folder.name
        assert c.local_release == TEST_RELEASE


@pytest.mark.chromeintern
def test_chromintern_latest_release():
    c = Chromintern()
    assert c.latest_release == powershell_get_latest_release()
