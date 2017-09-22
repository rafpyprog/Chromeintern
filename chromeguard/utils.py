'''
    Useful routines used by any OS
'''

import os
import re
import zipfile

import requests


def parse_chromedriver_version(cmd_stdout):
    '''
        cmd_stdout (string): Output from chromedriver -v
    '''
    CHROMEDRIVER_VERSION_PATTERN = '\d+\.\d+'
    version = re.search(CHROMEDRIVER_VERSION_PATTERN, cmd_stdout)
    if version:
        return version.group()
    else:
        raise Exception('Unable to parse Chromedriver version {}'
                        .format(cmd_stdout))


def API_get_latest_release():
    API_URL = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    response = requests.get(API_URL)
    response.raise_for_status()
    release = response.text.strip().replace(',', '.')
    return release


def unzip(file, path=None):
    if path is None:
        path = os.getcwd()

    with zipfile.ZipFile(file) as installer:
        installer.extractall(path)
        return os.path.join(path, installer.filelist[0].filename)
