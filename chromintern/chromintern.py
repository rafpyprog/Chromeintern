import os
from distutils.version import StrictVersion
import platform
import sys
from subprocess import check_output
import zipfile

import fire
import requests
from tqdm import tqdm

from . import __version__

from . import linux
from . import mac
from . import win


class Chromintern():
    def __init__(self):
        self.GOOGLE_API = 'https://chromedriver.storage.googleapis.com/'
        self.platform = platform.system()
        self.path = 'chromedriver'

    @property
    def local_release(self):
        functions = {'Linux': linux.get_local_release,
                     'Windows': win.get_local_release}

        get_release = functions[self.platform]
        release = get_release(executable_path=self.path)
        return release

    @property
    def latest_release(self):
        URL = self.GOOGLE_API + 'LATEST_RELEASE'
        response = requests.get(URL)
        response.raise_for_status()
        release = response.text.strip()
        return release

    @property
    def is_updated(self, executable_path='chromedriver'):
        return StrictVersion(self.local_release) == StrictVersion(self.latest_release)

    @property
    def installation_file(self):
        ''' Chromedriver installation file for OS '''
        install_files = {'darwin': mac.MAC_FILENAME,
                         'linux': linux.LINUX_FILENAME,
                         'win32': win.WIN_FILENAME}

        filename = install_files[sys.platform]
        return filename

    def download(self, version=None, path=None):
        if version is None:
            version = self.latest_release

        if path is None:
            path = os.getcwd()
        else:
            path = os.fspath(path)

        installation_file = self.installation_file
        version_file = '/'.join([str(version), installation_file])

        DOWNLOAD_URL = self.GOOGLE_API + version_file

        print('Downloading file: {}'.format(DOWNLOAD_URL))
        response = requests.get(DOWNLOAD_URL, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        path_to_save = os.path.join(path, installation_file)

        with open(path_to_save, 'wb') as f:
            for data in tqdm(iterable=response.iter_content(),
                             total=total_size, unit='B', unit_scale=True):
                f.write(data)
        return os.path.join(path, installation_file)


'''########################################################################'''


def unzip(file, path=None):
    if path is None:
        path = os.getcwd()
    else:
        path = os.fspath(path)
    with zipfile.ZipFile(file) as z:
        z.extractall(path)
        return os.path.join(path, z.filelist[0].filename)


def download(version=None, path=None, clean_up=True, set_environ=False):
    '''
        Download a Chromedriver release. If version is None, will download
        the lastest release.
    '''
    if path is None:
        path = os.getcwd()
    else:
        path = os.fspath(path)

    if version is None:
        version = get_latest_release()

    chrome_zip = _download(version, path=path)
    executable_path = unzip(chrome_zip, path=path)

    if sys.platform == 'linux':
        os.system('chmod +x ' + executable_path)

    # On windows we always keep the original zip file. It's use to determines
    # the version of the installed chromedriver
    if clean_up is True and platform.system() != 'Windows':
        os.remove(chrome_zip)

    if set_environ is True:
        environ_variable = 'CHROME_DRIVER_PATH'
        os.environ[environ_variable] = executable_path
        print('Chrome path {} on environ variable {}.'
              .format(executable_path, environ_variable))

    return executable_path




def get_chromedriver_path():
    path = None
    if platform.system() == 'Linux':
        cmd = ['which', 'chromedriver']
        path = check_output(cmd).decode().strip()
        path = os.path.dirname(path)
    elif platform.system() == 'Windows':
        path = win_path()
    else:
        #TO DO Windows, MAC
        pass

    if not path:
        raise FileNotFoundError('Could not find Chromedriver executable path.')
    return path


def update():
    installed_release = get_local_release()

    if is_updated():
        print('Chromedriver(v{}) already up-to-date.'
        .format(installed_release))
    else:
        print('Found existing installation: Chromedriver v{}'
              .format(installed_release))
        latest_release = get_latest_release()
        download(path=get_chromedriver_path())
        print('Successfully installed Chromedriver v{}'.format(latest_release))


#get_chrome(version='2.20', path=get_chromedriver_path())
if __name__ == '__main__':
    print('\nChromintern {}'.format(__version__.__version__))
    fire.Fire({'update': update, 'download': download})
