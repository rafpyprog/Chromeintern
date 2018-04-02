from unittest.mock import *

import pytest
import requests

from chromeguard import GoogleChrome, ChromeDriver


def get_latest_chrome_stable_version(os='linux'):
    # The Chrome team uses the OmahaProxy dashboard to keep track of current
    # versions in stable/beta/dev/canary.
    release_log = 'http://omahaproxy.appspot.com/all.json'
    r = requests.get(release_log)
    json = r.json()
    linux = [i for i in json if i['os'] == os][0]
    ver = [ver for ver in linux['versions'] if ver['channel'] == 'stable'][0]
    return ver['current_version']


def test_chrome_init():
    chrome = GoogleChrome()
    assert isinstance(chrome, GoogleChrome)


def test_parse_chrome_version():
    chrome = GoogleChrome()
    version = 'Google Chrome 65.0.3325.181'
    parsed_version = chrome.parse_chrome_version(version)
    assert parsed_version == 65


def test_chrome_version():
    chrome = GoogleChrome()
    version = chrome.version
    latest = get_latest_chrome_stable_version()
    assert version == chrome.parse_chrome_version(latest)


def test_chrome_find_compatible_chromedriver_version():
    CHROME_CLASS = 'chromeguard.GoogleChrome.version'
    with patch(CHROME_CLASS, new_callable=PropertyMock) as mock_ver:
        mock_ver.return_value = 62
        chrome = GoogleChrome()
        EXPECTED_VERSIONS = ['2.35', '2.34', '2.33']
        assert chrome.compatible_chromedriver_version == EXPECTED_VERSIONS
