import os
import platform
import pytest
import stat
import sys
from zipfile import ZipFile

from chromeguard import Guard
from chromeguard import linux
from chromeguard.linux import LINUX_FILENAME, linux_get_path
from chromeguard.mac import MAC_FILENAME
from chromeguard.win import WIN_FILENAME, get_local_release, win_get_path
from chromeguard.exceptions import NotUpdatedException
from chromeguard.utils import API_get_latest_release, unzip


APPVEYOR_PATH = 'C:\\Tools\\WebDriver'
TESTS_FOLDER = os.path.join(os.getcwd(), 'tests')
PLATFORM = platform.system()
TEST_RELEASE = '2.21'


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


@pytest.fixture(scope='session')
def installation_file():
    ''' Return the name of the zip file with the chromedriver executable for
    the platform '''
    if sys.platform == 'win32':
        installation_file = os.path.join(TESTS_FOLDER, WIN_FILENAME)
        #executable = os.path.join(TMP_PATH_FOLDER, 'chromedriver.exe')
    elif sys.platform == 'linux':
        installation_file = os.path.join(TESTS_FOLDER, linux.LINUX_FILENAME)
        #executable = os.path.join(TMP_PATH_FOLDER, 'chromedriver')
    return installation_file


###############################################################################
#  TMP FOLDER FOR CHROMEDRIER EXECUTABLE. SHOULD BE ON PATH
###############################################################################
@pytest.fixture(scope='session')
def tmp_local_driver(tmpdir_factory, installation_file):
    tmp_path = tmpdir_factory.getbasetemp()
    unzip(installation_file, path=tmp_path)

    executable = {'win32': 'chromedriver.exe', 'linux': 'chromedriver'}

    chromedriver_path = os.path.join(tmp_path, executable[sys.platform])
    yield chromedriver_path

    # Teardown
    os.remove(chromedriver_path)
    os.rmdir(tmp_path)


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
# LINUX ESPECIFIC FUNCTIONS
###############################################################################

@pytest.mark.linux
def test_chromedriver_tmp_path(tmp_local_driver):
        assert tmp_local_driver == os.path.join(TESTS_FOLDER, 'tmp_dir',
                                                'chromedriver')


@pytest.mark.linux
def test_chromedriver_is_executable_false(tmp_local_driver):
        assert not linux.is_allowed_to_execute(tmp_local_driver)


@pytest.mark.linux
def test_allow_to_execute_ok(tmp_local_driver):
    linux.allow_execution_as_program(tmp_local_driver)
    assert linux.is_allowed_to_execute(tmp_local_driver) is True


@pytest.mark.linux
def test_linux_get_local_release(tmp_local_driver):
    release = linux.get_local_release(tmp_local_driver)
    assert release == TEST_RELEASE


@pytest.mark.linux
def test_linux_get_path(tmp_local_driver):
    assert linux_get_path() == tmp_local_driver
    '''install chromedriver on tmp_dir and check if ok. Uninstall and
    then checj for raise'''
    pass

###############################################################################
# CHROMEGUARD - PLATFORM INDEPENDENT FUNCTIONS
###############################################################################

@pytest.mark.linux
@pytest.mark.Guard
def test_guard_get_local_release(tmp_local_driver):
    g = Guard()
    assert g.local_release == TEST_RELEASE


@pytest.mark.linux
@pytest.mark.Guard
def test_guard_latest_release():
    g = Guard()
    assert g.latest_release == API_get_latest_release()


@pytest.mark.linux
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
        msg = 'Platform not supported - {}'.format(sys.platform)
        raise EnvironmentError(msg)


@pytest.mark.linux
@pytest.mark.Guard
def test_guard_is_updated_false():
    ''' The test installation refers to release 2.20. Should return False '''
    g = Guard()
    assert g.is_updated is False


@pytest.mark.linux
@pytest.mark.Guard
def test_guard_is_updated_true(tmp_local_driver):
    '''  Download the latest release, insert on path. Should return True '''
    tmp_folder = os.path.dirname(tmp_local_driver)
    g = Guard()
    # download the latest release to the tmp path folder and unzi
    g.download(path=tmp_local_driver)
    zip_file = os.path.join(tmp_local_driver, g.installation_file)
    unzip(zip_file, tmp_local_driver)
    os.remove(zip_file)
    assert g.is_updated is True

@pytest.mark.linux
@pytest.mark.Guard
def test_guard_update_already_updated(tmp_local_driver):
    # Once the the latest update was installed in the last test check if the update
    # funtion will return none
    g = Guard()
    assert g.update() is None
    #g.download()
    #unzip(os.path.join(tmp_folder, g.installation_file), tmp_folder)
    # already updated retunr None


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
