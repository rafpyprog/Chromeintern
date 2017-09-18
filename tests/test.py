import os
import platform
import pytest
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from chromintern import Chromintern
from chromintern.linux import LINUX_FILENAME
from chromintern.mac import MAC_FILENAME
from chromintern.win import WIN_FILENAME, get_local_release, in_path, win_get_path
from chromintern.utils import powershell_get_latest_release, unzip


TESTS_FOLDER = os.path.join(os.getcwd(), 'tests')
PLATFORM = platform.system()
TEST_RELEASE = '2.20'
TMP_PATH_FOLDER = os.path.normpath(os.path.expanduser('~'))

@pytest.fixture
def tmp_folder():
    if sys.platform == 'win32':
        installation_file = os.path.join(TESTS_FOLDER, WIN_FILENAME)
        executable = os.path.join(TMP_PATH_FOLDER, 'chromedriver.exe')

    with ZipFile(installation_file) as z:
        z.extractall(TMP_PATH_FOLDER)

    yield TMP_PATH_FOLDER

    os.remove(executable)



###############################################################################
# WINDOWS ESPECIFIC FUNCTIONS
###############################################################################

@pytest.mark.windows
def test_win_get_local_release(tmp_folder):
    chrome_path = tmp_folder
    release = get_local_release(chrome_path)
    assert release == TEST_RELEASE


@pytest.mark.windows
def test_win_in_path_true(tmp_folder):
    assert in_path() is True


@pytest.mark.windows
def test_win_get_path_ok(tmp_folder):
    assert win_get_path() == TMP_PATH_FOLDER




###############################################################################
# CHROMINTERN - PLATFORM INDEPENDENT FUNCTIONS
###############################################################################

@pytest.mark.chromeintern
def test_chromintern_get_local_release(tmp_folder):
    c = Chromintern()
    c.path = tmp_folder
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
def test_chromintern_is_updated_false(tmp_folder):
    ''' The test installation refers to release 2.20. Should return False '''
    c = Chromintern()
    c.path = tmp_folder
    assert c.is_updated is False


@pytest.mark.chromeintern
def test_chromintern_is_updated_true(tmp_folder):
    '''  Download the latest release, insert on path. Should return True '''
    path = tmp_folder
    c = Chromintern()
    c.path = path
    # download the latest release to the tmp path folder and unzi
    c.download(path=path)
    unzip(os.path.join(path, c.installation_file), path)
    assert c.is_updated is True


@pytest.mark.chromeintern
def test_chromintern_download_latest_release(tmp_folder):
    c = Chromintern()
    c.download(path=tmp_folder)
    assert os.path.isfile(os.path.join(tmp_folder, c.installation_file))


@pytest.mark.chromeintern
def test_chromintern_update_already_updated(tmp_folder):
    path = tmp_folder
    c = Chromintern()
    c.path = path
    # download the latest release to the tmp path folder and unzi
    c.download(path=path)
    unzip(os.path.join(path, c.installation_file), path)
    # already updated retunr None
    assert c.update() is None

@pytest.mark.chromeintern
def test_chromintern_update(tmp_folder):
    c = Chromintern()
    c.path = tmp_folder
    c.update()
    assert c.is_updated is True
