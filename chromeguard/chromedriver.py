from io import BytesIO
import os
import re
from subprocess import PIPE, Popen
import shutil
from zipfile import is_zipfile, ZipFile

import requests


class ChromeDriver():
    GOOGLE_API = 'https://chromedriver.storage.googleapis.com/'

    def __init__(self, executable_path='chromedriver'):
        self.executable_path = executable_path

    def parse_chromedriver_version(self, stdout):
        '''
            cmd_stdout (string): Output from chromedriver -v
        '''
        CHROMEDRIVER_VERSION_PATTERN = '\d+\.\d+'
        version = re.search(CHROMEDRIVER_VERSION_PATTERN, stdout)
        if version:
            return version.group()
        else:
            raise Exception('Unable to parse Chromedriver version {}'
                            .format(stdout))

    @property
    def version(self):
        get_version_cmd = [self.executable_path, '-v']
        process = Popen(get_version_cmd, close_fds=True, stdout=PIPE,
                        universal_newlines=True)
        stdout, err = process.communicate()
        CHROMEDRIVER_VERSION_PATTERN = '\d+\.\d+'
        version = re.search(CHROMEDRIVER_VERSION_PATTERN, stdout).group()
        return version

    @property
    def latest_release(self):
        URL = self.GOOGLE_API + 'LATEST_RELEASE'
        response = requests.get(URL)
        response.raise_for_status()
        release = response.text.strip()
        return release

    def get_release_notes(self):
        release_notes_url = ''.join([self.GOOGLE_API, self.latest_release,
                                    '/notes.txt'])
        response = requests.get(release_notes_url)
        return response.text

    @property
    def releases(self):
        release_notes = self.get_release_notes()
        pattern = 'ChromeDriver\sv.*?Supports Chrome\sv[0-9]{2}-[0-9]{2}\n'
        releases = re.findall(pattern, release_notes, re.DOTALL)
        chromedriver = '(?<=ChromeDriver\sv).*?(?=\s)'
        google_chrome = '(?<=Chrome\sv).*(?=\n)'
        versions = []
        for release in releases:
            supported_chrome = re.search(google_chrome, release,
                                         re.DOTALL).group()
            min_version, max_version = supported_chrome.split('-')
            chromedriver_version = re.search(chromedriver, release).group()
            versions.append({'chromedriver': chromedriver_version,
                             'supported_chrome_versions': (int(min_version),
                                                           int(max_version))})
        return versions

    def find_compatible_chromedriver_version(self, chrome_version):
        releases = []
        for release in self.releases:
            min_version, max_version = release['supported_chrome_versions']
            if chrome_version in range(min_version, max_version + 1):
                releases.append(release['chromedriver'])
        return releases

    def supported_chrome_versions(self, chromedriver_version):
        for release in self.releases:
            if release['chromedriver'] == chromedriver_version:
                return release['supported_chrome_versions']
        return None

    def update(self, chrome_version=None, os='linux'):
        if chrome_version is not None:
            driver_version = self.find_compatible_chromedriver_version(chrome_version)[0]
        else:
            driver_version = self.latest_release

        installation_file = self.download(driver_version, os)
        install = self.install(installation_file)
        return install

    def download(self, driver_version, os):
        os_param = {'linux': 'linux64', 'windows': 'win32', 'mac': 'mac64'}
        URL = GOOGLE_API + '{}/chromedriver_{}.zip'.format(driver_version,
                                                           os_param[os])
        response = requests.get(URL)
        response.raise_for_status()
        installation_file = BytesIO(response.content)
        return installation_file

    def install(self, installation_file, path=None):
        assert zipfile.is_zipfile(installation_file) is True
        zip_file = ZipFile(installation_file)
        driver_binary = zip_file.namelist()[0]
        if path is None:
            path = os.path.dirname(shutil.which('chromedriver'))
        return zip_file.extract(driver_binary, path=path)
