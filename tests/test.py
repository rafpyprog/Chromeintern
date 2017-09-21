import os
import platform
import pytest
import sys
from zipfile import ZipFile

from chromeguard import Guard
from chromeguard.linux import LINUX_FILENAME
from chromeguard.mac import MAC_FILENAME
from chromeguard.win import WIN_FILENAME, get_local_release, win_get_path
from chromeguard.exceptions import NotUpdatedException
from chromeguard.utils import API_get_latest_release, unzip


APPVEYOR_PATH = 'C:\\Tools\\WebDriver'
TESTS_FOLDER = os.path.join(os.getcwd(), 'tests')
PLATFORM = platform.system()
TEST_RELEASE = '2.20'


def clean_up(executable):
    while True:
        try:
            os.remove(executable)
            while os.path.isfile(executable) is True:
                pass
        except PermissionError:
            pass
        else:
            break


@pytest.fixture
def tmp_folder():
    TMP_PATH_FOLDER = os.path.normpath(os.path.expanduser('~'))

    if sys.platform == 'win32':
        installation_file = os.path.join(TESTS_FOLDER, WIN_FILENAME)
        executable = os.path.join(TMP_PATH_FOLDER, 'chromedriver.exe')

    with ZipFile(installation_file) as z:
        z.extractall(TMP_PATH_FOLDER)
        z.close()

    yield TMP_PATH_FOLDER
    clean_up(executable)

###############################################################################
# WINDOWS ESPECIFIC FUNCTIONS
###############################################################################


@pytest.mark.windows
def test_win_get_local_release(tmp_folder):
    release = get_local_release(tmp_folder)
    assert release == TEST_RELEASE


@pytest.mark.windows
def test_win_get_path_ok(tmp_folder):
    assert win_get_path() in (tmp_folder, APPVEYOR_PATH)


###############################################################################
# CHROMEGUARD - PLATFORM INDEPENDENT FUNCTIONS
###############################################################################

@pytest.mark.Guard
def test_guard_get_local_release(tmp_folder):
    g = Guard(path=tmp_folder)
    assert g.local_release == TEST_RELEASE


@pytest.mark.Guard
def test_guard_latest_release():
    g = Guard()
    assert g.latest_release == API_get_latest_release()


@pytest.mark.Guard
def test_guard_installation_filename():
    g = Guard()
    if sys.platform == 'win32':
        assert g.installation_file == WIN_FILENAME
    elif sys.platform == 'darwin':
        assert g.installation_file == MAC_FILENAME
    elif sys.platform == 'linux':
        assert g.installation_file == LINUX_FILENAME
    else:
        raise 'Platform not supported - {}'.format(sys.platform)


@pytest.mark.Guard
def test_guard_is_updated_false(tmp_folder):
    ''' The test installation refers to release 2.20. Should return False '''
    g = Guard(path=tmp_folder)
    assert g.is_updated is False


@pytest.mark.Guard
def test_guard_is_updated_true(tmp_folder):
    '''  Download the latest release, insert on path. Should return True '''

    g = Guard(path=tmp_folder)
    # download the latest release to the tmp path folder and unzi
    g.download()
    unzip(os.path.join(tmp_folder, g.installation_file), tmp_folder)
    assert g.is_updated is True


@pytest.mark.Guard
def test_guard_download_latest_release(tmp_folder):
    g = Guard(path=tmp_folder)
    g.download()
    assert os.path.isfile(os.path.join(tmp_folder, g.installation_file))


@pytest.mark.Guard
def test_guard_update_already_updated(tmp_folder):
    g = Guard(path=tmp_folder)
    # download the latest release to the tmp path folder and unzi
    g.download()
    unzip(os.path.join(tmp_folder, g.installation_file), tmp_folder)
    # already updated retunr None
    assert g.update() is None


@pytest.mark.Guard
def test_guard_update(tmp_folder):
    g = Guard(path=tmp_folder)
    g.update()
    assert g.local_release == g.latest_release


@pytest.mark.Guard
def test_guard_raise_for_update(tmp_folder):
    g = Guard(path=tmp_folder)
    with pytest.raises(NotUpdatedException):
        g.raise_for_update()
