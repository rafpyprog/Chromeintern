import re
import os
import platform
from zipfile import is_zipfile

import pytest
import requests

from chromeguard import ChromeDriver


def test_chromedriver_init():
    driver = ChromeDriver()
    assert isinstance(driver, ChromeDriver)


def test_parse_chromedriver_version():
    driver = ChromeDriver()
    VERSION = ('ChromeDriver 2.37.544315 (730aa6a5fdba159ac9f4c1e8cbc59bf1b5ce'
               '12b7)')
    parsed_version = driver.parse_chromedriver_version(VERSION)
    EXPECTED_VERSION = '2.37'
    assert parsed_version == EXPECTED_VERSION


def test_latest_chromedriver():
    LATEST_URL = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    latest_release = requests.get(LATEST_URL).text.strip()
    driver = ChromeDriver()
    assert driver.latest_release == latest_release


def test_get_release_notes():
    driver = ChromeDriver()
    latest = driver.latest_release
    notes = driver.get_release_notes()
    assert isinstance(notes, str)
    PATTERN = 'ChromeDriver v' + latest + ' \([0-9]{4}-[0-9]{2}-[0-9]{2}\)'
    notes_validation = re.search(PATTERN, notes)
    assert notes_validation is not None


def test_download_chromedriver():
    driver = ChromeDriver()
    installation_file = driver.download(driver.latest_release, os='linux')
    assert is_zipfile(installation_file) is True


def test_install_chromedriver():
    driver = ChromeDriver()
    os_name = platform.system().lower()
    installation_file = driver.download(driver.latest_release, os=os_name)
    path = driver.install(installation_file, path='.')
    assert path == 'chromedriver'
    os.remove('chromedriver')
