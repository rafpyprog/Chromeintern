import os
from distutils.version import StrictVersion
import platform
import sys

import requests
from tqdm import tqdm

from . import linux
from . import mac
from . import win
from . exceptions import NotUpdatedException
from .utils import unzip


class Guard():
    def __init__(self, path=None):
        self.GOOGLE_API = 'https://chromedriver.storage.googleapis.com/'
        self.platform = platform.system()
        self.path = path or 'chromedriver'

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
        local = StrictVersion(self.local_release)
        latest = StrictVersion(self.latest_release)
        return local == latest

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
            path = self.path

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

    def update(self):
        if self.is_updated is True:
            print('Chromedriver(v{}) already up-to-date.'
                  .format(self.local_release))
            return None
        else:
            print('Found existing installation: Chromedriver v{}'
                  .format(self.local_release))

            installation_file = self.download(path=self.path)
            unzip(installation_file, path=self.path)

            print('Successfully installed Chromedriver v{}'
                  .format(self.local_release))
            return True

    def raise_for_update(self):
        ''' Raises NotUpdatedException if installed Chromedriver is not
            updated
        '''
        if self.is_updated is False:
            raise NotUpdatedException(self.local_release, self.latest_release)
