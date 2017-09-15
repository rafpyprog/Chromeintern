import os
import platform
import pytest
import sys
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
    with ZipFile(os.path.join(TESTS_FOLDER, WIN_FILENAME)) as z:
        z.extractall(tmp.name)
    yield tmp
    tmp.cleanup()


###############################################################################
# WINDOWS ESPECIFIC FUNCTIONS
###############################################################################

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


###############################################################################
# CHROMINTERN - PLATFORM INDEPENDENT FUNCTIONS
###############################################################################

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


@pytest.mark.chromeintern
def test_chromintern_installation_file():
    c = Chromintern()
    if sys.platform == 'win32':
        assert c.installation_file == WIN_FILENAME
    elif sys.platform == 'darwin':
        assert c.installation_file == MAC_FILENAME
    elif sys.platform == 'linux':
        assert c.installation_file == LINUX_FILENAME
    else:
        raise 'Platform not supported - {}'.format(sys.platform)


@pytest.mark.chromeintern
def test_chromintern_download_latest_release(tmp_folder):
    with tmp_folder:
        c = Chromintern()
        c.download(path=tmp_folder.name)
        assert os.path.isfile(os.path.join(tmp_folder.name,
                                           c.installation_file))
